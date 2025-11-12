from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap

PathLike = Union[str, Path]

class ImageProvider:
    """
    Traduce 'valor' del modelo -> QPixmap, cargando desde ui/images/.
    - Cachea pixmaps (por archivo).
    - Aplica fallback si el archivo no existe.
    - Opcional: devuelve copia escalada si pasas 'target_size'.
    """
    # Extensiones probadas en orden
    _EXTS = (".png", ".jpg", ".jpeg")

    def __init__(self, base_dir: Optional[PathLike] = None) -> None:
        if base_dir is None:
            # .../ui/recursos/image_provider.py -> .../ui/images
            base_dir = Path(__file__).resolve().parent.parent / "images"
        self.base_dir = Path(base_dir)
        self._cache: Dict[Path, QPixmap] = {}

        # Dorso por convención: back.png (o jpg)
        self._back_pixmap = self._load_first_existing("back")

    # ------------- API pública -------------

    def pixmap_for_value(
        self,
        valor: Union[int, str],
        target_size: Optional[Union[QSize, Tuple[int, int]]] = None,
    ) -> QPixmap:
        """
        Devuelve el QPixmap para 'valor'.
        Si se pasa 'target_size', devuelve copia escalada (manteniendo aspecto).
        """
        pm = self._load_first_existing(str(valor))
        if target_size:
            size = self._coerce_size(target_size)
            return pm.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pm

    def pixmap_back(
        self,
        target_size: Optional[Union[QSize, Tuple[int, int]]] = None,
    ) -> QPixmap:
        pm = self._back_pixmap or self._placeholder_pixmap("BACK")
        if target_size:
            size = self._coerce_size(target_size)
            return pm.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pm

    # ------------- Internas -------------

    def _coerce_size(self, s: Union[QSize, Tuple[int, int]]) -> QSize:
        if isinstance(s, QSize):
            return s
        w, h = s
        return QSize(int(w), int(h))

    def _load_first_existing(self, stem: str) -> QPixmap:
        """
        Busca stem.{png|jpg|jpeg} en base_dir. Si no existe, placeholder.
        Cachea por ruta real.
        """
        for ext in self._EXTS:
            p = self.base_dir / f"{stem}{ext}"
            if p.exists():
                return self._get_or_load(p)
        # No existe → placeholder
        return self._placeholder_pixmap(stem)

    def _get_or_load(self, path: Path) -> QPixmap:
        pm = self._cache.get(path)
        if pm is not None:
            return pm
        pm = QPixmap(str(path))
        if pm.isNull():
            # Fichero corrupto o no cargable → placeholder
            pm = self._placeholder_pixmap(path.stem)
        self._cache[path] = pm
        return pm

    def _placeholder_pixmap(self, text: str, size: Tuple[int, int] = (256, 256)) -> QPixmap:
        """
        Genera una imagen de relleno con fondo y texto centrado (útil en dev).
        """
        w, h = size
        pm = QPixmap(w, h)
        pm.fill(QColor("#2b2d42"))  # gris azulado
        painter = QPainter(pm)
        painter.setPen(QColor("white"))
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(pm.rect(), Qt.AlignCenter, text)
        painter.end()
        return pm
