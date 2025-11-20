from PySide6.QtGui import QTextCursor

class MarkdownOperations:
	def wrap_inline(self, cursor: QTextCursor, left: str, right: str | None = None) -> None:
		"""Envolver selección con marcadores (p. ej., '**', '_')."""

	def toggle_bold(self, cursor: QTextCursor) -> None:
		self.wrap_inline(cursor, "**")

	def toggle_italic(self, cursor: QTextCursor) -> None:
		self.wrap_inline(cursor, "_")

	def toggle_heading(self, cursor: QTextCursor, level: int) -> None:
		"""Prefija '# ' o '## ' o '### ' a cada línea seleccionada (toggle si ya está)."""

	def toggle_list(self, cursor: QTextCursor) -> None:
		"""Prefija '- ' por línea (toggle)."""

	def block_code(self, cursor: QTextCursor) -> None:
		"""Envuelve el bloque con ``` ... ``` (si ya está, quita)."""

	def insert_hr(self, cursor: QTextCursor) -> None:
		cursor.insertText("\n\n---\n\n")

	def insert_table_template(self, cursor: QTextCursor) -> None:
		cursor.insertText("\n| Col1 | Col2 |\n|------|------|\n|  ..  |  ..  |\n")

	def insert_link(self, cursor: QTextCursor) -> None:
		"""Si hay selección -> [sel](url), si no -> [](url) y posicionar el cursor entre []."""
