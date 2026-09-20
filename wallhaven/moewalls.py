import html
import re
import urllib.parse
from typing import Optional
import requests
from wallhaven.api import WallpaperItem, SearchResult

MOEWALLS_BASE_URL = "https://moewalls.com"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

CATEGORIES = [
    ("all", "All"),
    ("anime", "Anime"),
    ("games", "Games"),
    ("sci-fi", "Sci-Fi"),
    ("fantasy", "Fantasy"),
    ("landscape", "Landscape"),
    ("pixel-art", "Pixel Art"),
    ("animal", "Animals"),
    ("vehicle", "Vehicles"),
    ("movies", "Movies"),
    ("lifestyle", "Lifestyle"),
    ("abstract", "Abstract"),
    ("others", "Others"),
]


class MoeWallsManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,cs;q=0.8",
        })
        self._detail_cache: dict[str, WallpaperItem] = {}

    def get_categories(self) -> list[tuple[str, str]]:
        return CATEGORIES

    def search(
        self,
        query: str = "",
        category: str = "all",
        page: int = 1,
    ) -> SearchResult:
        """
        Searches or browses MoeWalls animated wallpapers.
        Returns SearchResult with WallpaperItem objects having is_animated=True.
        """
        query = query.strip()
        category = category.strip().lower()

        if query:
            if page > 1:
                url = f"{MOEWALLS_BASE_URL}/page/{page}/?s={urllib.parse.quote(query)}"
            else:
                url = f"{MOEWALLS_BASE_URL}/?s={urllib.parse.quote(query)}"
        elif category and category != "all":
            if page > 1:
                url = f"{MOEWALLS_BASE_URL}/category/{category}/page/{page}/"
            else:
                url = f"{MOEWALLS_BASE_URL}/category/{category}/"
        else:
            if page > 1:
                url = f"{MOEWALLS_BASE_URL}/page/{page}/"
            else:
                url = f"{MOEWALLS_BASE_URL}/"

        resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        content = resp.text

        articles = re.findall(
            r'<article[^>]*class=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</article>',
            content,
            re.DOTALL,
        )

        items: list[WallpaperItem] = []
        for cls, body in articles:
            # 1. Title & Link
            m_link = re.search(r'<a[^>]+title=[\"\']([^\"\']+)[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', body)
            if not m_link:
                m_link = re.search(r'<a[^>]+href=[\"\']([^\"\']+)[\"\'][^>]+title=[\"\']([^\"\']+)[\"\']', body)
            if not m_link:
                continue

            title = html.unescape(m_link.group(1).strip())
            link = m_link.group(2).strip()

            # 2. Thumbnail
            m_img = re.search(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', body)
            thumb = m_img.group(1).strip() if m_img else ""

            # 3. Resolution
            m_res = re.search(r'resolutions-(\d+x\d+)', cls)
            res_str = m_res.group(1) if m_res else "1920x1080"
            dim_x, dim_y = (int(x) for x in res_str.split("x")) if "x" in res_str else (1920, 1080)

            # 4. Item ID
            m_id = re.search(r'post-(\d+)', cls)
            item_id = f"mw_{m_id.group(1)}" if m_id else f"mw_{link.strip('/').split('/')[-1]}"

            # 5. Category
            m_cat = re.search(r'category-([a-zA-Z0-9_-]+)', cls)
            cat_name = m_cat.group(1).replace("-", " ").title() if m_cat else "Anime"

            tags = [{"name": "Live Wallpaper"}, {"name": cat_name}]

            item = WallpaperItem(
                id=item_id,
                url=link,
                short_url=link,
                views=0,
                favorites=0,
                source="MoeWalls",
                purity="sfw",
                category=cat_name.lower(),
                dimension_x=dim_x,
                dimension_y=dim_y,
                resolution=res_str,
                ratio="16:9",
                file_size=0,
                file_type="video/mp4",
                created_at="",
                colors=[],
                path=link,  # Initial path is article URL, resolved to download URL on detail or download
                thumb_large=thumb,
                thumb_small=thumb,
                thumb_original=thumb,
                tags=tags,
                uploader={"username": "MoeWalls"},
                is_animated=True,
                preview_video_url="",
            )
            # Store title for convenient display
            item._display_title = title
            items.append(item)

        # Pagination detection
        pages = [int(p) for p in re.findall(r'/page/(\d+)/', content)]
        last_page = max(pages, default=page)
        if last_page < page:
            last_page = page

        # Approximate total
        total = last_page * 16

        return SearchResult(
            items=items,
            current_page=page,
            last_page=last_page,
            per_page=16,
            total=total,
        )

    def get_wallpaper_detail(self, item: WallpaperItem) -> WallpaperItem:
        """
        Fetches detailed information for a MoeWalls wallpaper:
        resolves preview video URL and direct download MP4 URL.
        """
        if item.id in self._detail_cache:
            return self._detail_cache[item.id]

        article_url = item.url
        resp = self.session.get(article_url, timeout=15)
        resp.raise_for_status()
        content = resp.text

        # 1. Preview Video WebM / MP4
        v_m = re.search(r'<source[^>]+src=[\"\']([^\"\']+)[\"\']', content)
        preview_video = v_m.group(1) if v_m else ""
        if preview_video and preview_video.startswith("/"):
            preview_video = MOEWALLS_BASE_URL + preview_video

        # 2. Download MP4 URL
        dl_m = re.search(
            r'id=[\"\']moe-download[\"\'][^>]*data-url=[\"\']([^\"\']+)[\"\']',
            content,
        ) or re.search(
            r'data-url=[\"\']([^\"\']+)[\"\'][^>]*id=[\"\']moe-download[\"\']',
            content,
        )
        if dl_m:
            download_url = f"https://go.moewalls.com/download.php?video={dl_m.group(1)}"
        else:
            mp4_m = re.search(r'https?://[^\s\"\'<>]+\.mp4', content)
            download_url = mp4_m.group(0) if mp4_m else item.url

        # 3. Tags
        tag_matches = re.findall(
            r'<a[^>]+href=[\"\']https://moewalls\.com/tag/[^\"\']+[\"\'][^>]*>(.*?)</a>',
            content,
        )
        tags = []
        for t in tag_matches:
            clean = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
            if clean and not any(x["name"].lower() == clean.lower() for x in tags):
                tags.append({"name": clean})

        if not tags:
            tags = item.tags

        # Update item fields
        item.preview_video_url = preview_video
        item.path = download_url
        item.tags = tags

        self._detail_cache[item.id] = item
        return item

    def get_download_url(self, item: WallpaperItem) -> str:
        """Returns direct downloadable MP4 URL for the item."""
        if item.path.startswith("http") and ("go.moewalls.com" in item.path or item.path.endswith(".mp4")):
            return item.path
        enriched = self.get_wallpaper_detail(item)
        return enriched.path


moewalls_manager = MoeWallsManager()
