"""
CAPA DE VISTA: VENTANA PRINCIPAL DE LA APLICACION
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QListWidget, QListWidgetItem,  QTableWidgetItem, QVBoxLayout, QComboBox, QTableWidget
from PySide6.QtGui import QAction
from services.data_services import DataService

"""
    VENTANA PRINCIPAL DE LA APLICACION
    CONTIENE EL MENU, EL COMBOBOX Y LA TABLA DE DATOS
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.setWindowTitle("Aplicacion con PySide6 con Aquitectura en Capas - Gestión de Datos")
        self.__init_ventana()
        self.__crear_menu()
        self.__crear_interfaz()

    def __init_ventana(self, x:int, y:int, w:int, h:int) -> None:
        # Parametrizar setGeometry desde sysargv
        self.setGeometry(100, 100, 600, 400)
        self.crear_menu()

    def __crear_menu(self) -> None:
        menubar = self.menuBar()
        menu_datos = menubar.addMenu("&Datos")
        action_combobox = QAction("Poblar &Combobox", self)

        action_combobox.setStatusTip("Poblar el ComboBox con datos")
        action_combobox.triggered.connect(self.__poblar_combobox())
        menu_datos.addAction(action_combobox)

        action_listado = QAction("Poblar &Listado", self)
        action_listado.setStatusTip("Poblar el listado con datos")
        action_listado.triggered.connect(self.__poblar_listado())
        menu_datos.addAction(action_listado)

        menu_datos.addSeparator()

        action_salir = QAction("&Salir", self)
        action_salir.setStatusTip("Salir de la aplicación")
        action_salir.triggered.connect(self.__close())
        menu_datos.addAction(action_salir)

    def __crear_interfaz(self) -> None:
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout = QVBoxLayout()
        widget_central.setLayout(layout)

        self.combobox = QComboBox()
        self.combobox.addItem("-- Selecciona una opción --")
        layout.addWidget(self.combobox)

        self.listado = QListWidget()
        layout.addWidget(self.listado)

        self.statusBar().showMessage("Listo")

    def __poblar_combobox(self) -> None:
        try:
            self.combobox.clear()
            
            datos:str = self.data_service.obtener_datos_combobox()
            lista = datos.split("\n")

            for i in lista:
                self.combobox.addItem(i)
            
            self.statusBar().showMessage("ComboBox poblado correctamente. Cargadas "+ self.combobox.count() +" opciones.")
        except Exception as e:
            self.statusBar().showMessage(f"Error al poblar el combobox: {str(e)}")

    def __poblar_lista(self) -> None:
        try:
            self.listado.clear()
            
            lineas:str = self.data_service.obtener_datos_tabla()
            datos_encabezado = lineas[0].strip().split(",")

            self.listado.addItem(" | ".join(datos_encabezado))
            self.listado.addItem("-" * 50)

            for linea in lineas[1:]:
                campos = linea.strip().split(",")
                item_text = " | ".join(campos)
                self.listado.addItem(item_text)
            self.statusBar().showMessage("Listado poblado correctamente. Cargadas " + self.listado.count()+ " opciones.")
        except Exception as e:
            self.statusBar().showMessage(f"Error al poblar la lista: {str(e)}")