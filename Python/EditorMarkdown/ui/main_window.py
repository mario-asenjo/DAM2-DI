from __future__ import annotations

from typing import Optional

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
	QMainWindow, QWidget, QPlainTextEdit, QStatusBar, QVBoxLayout,
	QHBoxLayout, QGridLayout, QPushButton, QComboBox
)

class MainWindow(QMainWindow):
	"""
	EDITOR MD: Zona superior: editor ocupando todo el ancho.
			   Zona inferior: panel con dos areas:
					Izquierda: Botones md.
					Derecha: Abrir .txt y cerrar .md
	"""

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent)
		self.setWindowTitle("Editor Markdown Mario Asenjo")
		self.resize(1000, 700)

		# --- Menú básico ---
		self._crear_menu()

		# --- Barra de estado (feedback, ruta, modificado, etc.) ---
		self.setStatusBar(QStatusBar(self))

		# --- Widget Central LVertical : editor arriba, botones abajo ---
		contenedor = QWidget(self)
		vbox = QVBoxLayout(contenedor)
		vbox.setContentsMargins(8, 8, 8, 8)
		vbox.setSpacing(10)

		# --- Zona superior del Widget Central (4/5) ---
		self.editor = QPlainTextEdit(contenedor)
		self.editor.setPlaceholderText("Escribe aquí el texto a convertir máquina!!!!")
		# Ajuste de línea activado por defecto
		self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

		# --- Zona inferior del Widget Central (1/5) ---
		panel_inferior = QWidget(contenedor)
		hbox = QHBoxLayout(panel_inferior)
		hbox.setContentsMargins(0, 0, 0, 0)
		hbox.setSpacing(100)

		# --- Panel botones MD (izquierda 70%) ---
		panel_md = QWidget(panel_inferior)
		grid = QGridLayout(panel_md)
		grid.setContentsMargins(30, 0, 0, 0)
		grid.setHorizontalSpacing(8)
		grid.setVerticalSpacing(6)

		# --- Filas Botones ---
		# Fila 1: Titulos, Lista, Código, Tabla
		self.cmb_titulos = QComboBox(panel_md)
		self.cmb_titulos.addItems(["Titulo h1", "Titulo h2", "Titulo h3", "Titulo h4"])
		self.btn_lista = QPushButton("Lista", panel_md)
		self.btn_codigo = QPushButton("Bloque código", panel_md)
		self.btn_tabla = QPushButton("Tabla", panel_md)

		# Fila 2: Enlace, Separador, Cursiva, Negrita
		self.btn_enalce = QPushButton("Enlace", panel_md)
		self.btn_separador = QPushButton("Separador", panel_md)
		self.btn_cursiva = QPushButton("Cursiva", panel_md)
		self.btn_negrita = QPushButton("Negrita", panel_md)

		# --- Añadir botones al grid ---
		grid.addWidget(self.cmb_titulos, 0, 1)
		grid.addWidget(self.btn_lista, 0, 2)
		grid.addWidget(self.btn_codigo, 0, 3)
		grid.addWidget(self.btn_tabla, 0, 4)
		grid.addWidget(self.btn_enalce, 1, 1)
		grid.addWidget(self.btn_separador, 1, 2)
		grid.addWidget(self.btn_cursiva, 1, 3)
		grid.addWidget(self.btn_negrita, 1, 4)

		# --- Panel de Archivo ---
		panel_archivo = QWidget(panel_inferior)
		hfile = QHBoxLayout(panel_archivo)
		hfile.setContentsMargins(0, 0, 0, 0)
		hfile.setSpacing(8)

		self.btn_abrir = QPushButton("Abrir .txt...", panel_archivo)
		self.btn_guardar = QPushButton("Guardar .md...", panel_archivo)

		hfile.addWidget(self.btn_abrir)
		hfile.addWidget(self.btn_guardar)
		hfile.addStretch(1)

		# --- Nombrado de objetos para estilar con QSS ---
		self.editor.setObjectName("editor")
		panel_md.setObjectName("panel_md")
		panel_archivo.setObjectName("panel_archivo")

		# --- Composición del panel inferior: 70/30 con stretch
		hbox.addWidget(panel_md, stretch=7)
		hbox.addWidget(panel_archivo, stretch=3)

		# --- Añadir al layout vertical con proporcion 4/5 y 1/5 ---
		vbox.addWidget(self.editor, stretch=4)
		vbox.addWidget(panel_inferior, stretch=1)

		self.setCentralWidget(contenedor)

	def _crear_menu(self) -> None:
		menu = self.menuBar().addMenu("&Archivo")

		# QAction con sus comandos en texto, sus atajos y sus señales
		self.act_abrir = QAction("Abrir...", self)
		self.act_guardar = QAction("Guardar...", self)
		self.act_salir = QAction("Salar...", self)

		self.act_abrir.setShortcut(QKeySequence.StandardKey.Open)
		self.act_guardar.setShortcut(QKeySequence.StandardKey.Save)
		self.act_salir.setShortcut(QKeySequence.StandardKey.Close)

		menu.addAction(self.act_abrir)
		menu.addAction(self.act_guardar)
		menu.addSeparator()
		menu.addAction(self.act_salir)

		self.act_abrir.triggered.connect(self.on_open_txt)
		self.act_guardar.triggered.connect(self.on_save_md)
		self.act_salir.triggered.connect(self.on_exit)

	# STUBS -> SOLO MENSAJES EN LA STATUSBAR
	def on_open_txt(self) -> None:
		self.statusBar().showMessage("Abrir .txt... (stub)", 1500)

	def on_save_md(self) -> None:
		self.statusBar().showMessage("Guardar .md... (stub)", 1500)

	def on_exit(self) -> None:
		self.statusBar().showMessage("Salir (stub)", 1500)