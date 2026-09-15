# Maintainer: Sedly12322 <d.sedlar41@gmail.com>
pkgname=wallhaven-desktop-git
_pkgname=wallhaven-desktop
pkgver=1.0.0.r2.ge5b356f
pkgrel=1
pkgdesc="Modern dark-themed Wallhaven wallpaper browser and downloader for Arch Linux / Hyprland"
arch=('any')
url="https://github.com/Sedly12322/wallhaven-desktop"
license=('MIT')
depends=(
    'python'
    'python-pyqt6'
    'python-requests'
    'python-pillow'
)
makedepends=(
    'git'
    'python-build'
    'python-installer'
    'python-wheel'
    'python-setuptools'
)
optdepends=(
    'libnotify: Desktop notifications'
    'swww: Wayland wallpaper daemon'
    'mpvpaper: Video wallpaper player'
    'feh: X11 wallpaper setter'
)
provides=("$_pkgname")
conflicts=("$_pkgname")
source=("git+https://github.com/Sedly12322/wallhaven-desktop.git")
sha256sums=('SKIP')

pkgver() {
    cd "$srcdir/$_pkgname"
    printf "1.0.0.r%s.g%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
    cd "$srcdir/$_pkgname"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$_pkgname"
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Desktop shortcut
    install -Dm644 wallhaven-desktop.desktop "$pkgdir/usr/share/applications/wallhaven-desktop.desktop"

    # Application icon
    install -Dm644 assets/icon.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/wallhaven-desktop.png"

    # License
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
