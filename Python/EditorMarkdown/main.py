from PySide6.QtWidgets import QApplication, QStyleFactory
import sys
from pathlib import Path

from ui.main_window import MainWindow
from ui.styles.DarkPalette import DarkPalette

def main() -> None:
	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create("Fusion"))
	app.setPalette(DarkPalette())
	qss_path = Path(__file__).parent / "ui" / "styles" / "dark.qss"
	app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()