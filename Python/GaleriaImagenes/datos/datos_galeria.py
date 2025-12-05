from pathlib import Path

APP_DIR: Path = Path(__file__).resolve().parent.parent
UI_DIR: Path = APP_DIR / "ui"
EXTENSIONES: set[str] = {".png", ".jpg", ".jpeg"}