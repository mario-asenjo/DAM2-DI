from PySide6.QtGui import QPalette, QColor


class DarkPalette(QPalette):
    def __init__(self):
        super().__init__()
        self.setColor(QPalette.Window, QColor("#121212"))
        self.setColor(QPalette.WindowText, QColor("#f0f0f0"))
        self.setColor(QPalette.Base, QColor("#1c1c1c"))
        self.setColor(QPalette.Text, QColor("#e6e6e6"))
        self.setColor(QPalette.Button, QColor("#1f1f1f"))
        self.setColor(QPalette.ButtonText, QColor("#eaeaea"))
        self.setColor(QPalette.Highlight, QColor("#3d6cff"))
        self.setColor(QPalette.HighlightedText, QColor("#ffffff"))