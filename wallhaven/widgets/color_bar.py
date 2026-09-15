from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
)

WALLHAVEN_COLORS = [
    ("660000", "Tmavě červená"),
    ("cc0000", "Červená"),
    ("ea4c88", "Růžová"),
    ("993399", "Fialová"),
    ("333399", "Tmavě modrá"),
    ("0066cc", "Královská modrá"),
    ("0099ff", "Světle modrá"),
    ("66cccc", "Tyrkysová"),
    ("77cc33", "Světle zelená"),
    ("336600", "Tmavě zelená"),
    ("ffff00", "Žlutá"),
    ("ff9900", "Oranžová"),
    ("ff6600", "Jantarová"),
    ("663300", "Hnědá"),
    ("000000", "Černá"),
    ("424153", "Břidlicová"),
    ("999999", "Šedá"),
    ("ffffff", "Bílá"),
]


class ColorButton(QPushButton):
    def __init__(self, hex_color: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        self.hex_color = hex_color
        self.setToolTip(tooltip or f"#{hex_color}")
        self.setFixedSize(22, 22)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_style(False)

    def update_style(self, checked: bool):
        border = "2px solid #ffffff" if checked else "1px solid #44475a"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #{self.hex_color};
                border: {border};
                border-radius: 11px;
            }}
            QPushButton:hover {{
                border: 2px solid #6366f1;
            }}
        """)


class ColorBar(QFrame):
    color_changed = pyqtSignal(str)  # Emits hex code without '#' or "" if reset

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("colorBarFrame")
        self.selected_color = ""
        self.buttons: list[ColorButton] = []
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        title = QLabel("Barva:")
        title.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 11px;")
        layout.addWidget(title)

        for hex_code, name in WALLHAVEN_COLORS:
            btn = ColorButton(hex_code, name)
            btn.clicked.connect(lambda checked, c=hex_code, b=btn: self._on_color_clicked(c, b))
            layout.addWidget(btn)
            self.buttons.append(btn)

        self.clear_btn = QPushButton("✕ Všechny")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: #252833;
                color: #94a3b8;
                border: 1px solid #3b3f4d;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #323644;
                color: #e2e8f0;
            }
        """)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_selection)
        layout.addWidget(self.clear_btn)

        layout.addStretch()

    def _on_color_clicked(self, hex_code: str, clicked_btn: ColorButton):
        if self.selected_color == hex_code:
            # Deselect
            self.selected_color = ""
            clicked_btn.setChecked(False)
            clicked_btn.update_style(False)
        else:
            self.selected_color = hex_code
            for btn in self.buttons:
                is_this = (btn == clicked_btn)
                btn.setChecked(is_this)
                btn.update_style(is_this)

        self.color_changed.emit(self.selected_color)

    def clear_selection(self):
        self.selected_color = ""
        for btn in self.buttons:
            btn.setChecked(False)
            btn.update_style(False)
        self.color_changed.emit("")

    def set_color(self, hex_code: str):
        self.selected_color = hex_code.lower()
        for btn in self.buttons:
            is_this = (btn.hex_color.lower() == self.selected_color)
            btn.setChecked(is_this)
            btn.update_style(is_this)
