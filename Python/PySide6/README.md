# Mi primer Hola Mundo con PySide6

## Contexto

Este proyecto es una guía paso a paso para crear tu primera aplicación de escritorio en **Python** utilizando **PySide6 (Qt for Python)**.  
El objetivo es mostrar cómo configurar un entorno virtual, instalar dependencias, crear una ventana básica y entender el ciclo de vida de una aplicación Qt.

> 💡 Proyecto realizado en clase como práctica inicial de interfaces gráficas con PySide6.

**Repositorio del proyecto:** [enlace a tu GitHub aquí]

---

## Objetivos de aprendizaje

- Crear y activar un entorno virtual de Python.  
- Instalar y usar **PySide6**.  
- Comprender qué es `QApplication` y cómo funciona el ciclo de eventos (`app.exec()`).  
- Crear una ventana básica con un `QLabel` que muestre “Hola Mundo”.  
- Separar el código en un punto de entrada (`main.py`) y una clase de ventana (`ventana.py`).

---

## Requisitos previos

| Requisito | Versión / Herramienta |
|------------|------------------------|
| Python     | 3.11 (recomendado)     |
| Sistema operativo | Windows 10/11 o macOS/Linux |
| Editor de código | Visual Studio Code (u otro) |
| Control de versiones | Git |

---

## Creación y activación del entorno virtual

### En Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### En macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Verifica el entorno activo

```bash
where python   # Windows
which python   # macOS/Linux
python --version
```

Asegúrate de que la ruta del intérprete corresponde a tu carpeta `venv/`.

---

## Instalación de dependencias

Instala PySide6:

```bash
pip install PySide6
```

Exporta las dependencias a un archivo:

```bash
pip freeze > requirements.txt
```

### ¿Qué es PySide6?

**PySide6** es el *binding oficial* de **Qt6** para Python.  
Permite crear interfaces gráficas nativas multiplataforma (Windows, macOS y Linux) usando las clases de Qt (ventanas, botones, etiquetas, layouts, etc.).

 [Documentación oficial de PySide6](https://doc.qt.io/qtforpython/)

---

## Estructura mínima del proyecto

```bash
proyecto-hola-mundo/
 ├─ src/
 │  ├─ main.py          # punto de entrada
 │  └─ ventana.py       # clase Ventana
 ├─ .gitignore
 ├─ requirements.txt
 └─ README.md
```

La separación entre `main.py` y `ventana.py` facilita el mantenimiento y la escalabilidad.  
Cada módulo tiene una única responsabilidad: uno arranca la app y otro define la interfaz.

---

## Código fuente con explicación

### `src/ventana.py`

```python
# ventana.py
from PySide6.QtWidgets import QMainWindow, QLabel

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Mi primera ventana con PySide6")
        self.setGeometry(100, 100, 400, 200)

        # Creamos un QLabel (widget de texto)
        etiqueta = QLabel("¡Hola Mundo con PySide6!", self)
        etiqueta.move(120, 80)  # Posición dentro de la ventana
```

**Explicación:**

- `QMainWindow` → Clase base para ventanas principales.
- `setWindowTitle()` → Cambia el título de la ventana.
- `setGeometry()` → Define posición y tamaño (x, y, ancho, alto).
- `QLabel` → Widget para mostrar texto.
- `move()` → Coloca el widget dentro de la ventana.

---

### `src/main.py`

```python
# main.py
import sys
from PySide6.QtWidgets import QApplication
from ventana import Ventana

# Punto de entrada principal
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea la aplicación Qt
    ventana = Ventana()           # Instancia la ventana
    ventana.show()                # Muestra la interfaz
    sys.exit(app.exec())          # Inicia el bucle de eventos
```

**Explicación clave:**

- `QApplication` → Obligatoria en toda app Qt, gestiona el bucle de eventos.
- `ventana.show()` → Hace visible la ventana.
- `app.exec()` → Inicia el bucle principal (la app se mantiene abierta).
- `sys.exit()` → Asegura un cierre limpio al terminar.

---

## Ejecución y prueba

Desde la carpeta `src/`, ejecuta:

```bash
python main.py
```

Deberías ver una ventana con el título **"Mi primera ventana con PySide6"** y el texto **"¡Hola Mundo con PySide6!"**.

#### FUTURO PNG AQUI!!!!

---

## Variaciones sugeridas

Puedes cambiar el texto o el título de la ventana:

```python
self.setWindowTitle("Mi Ventana Personalizada")
etiqueta.setText("¡Hola desde otra versión!")
```

---

## Problemas frecuentes

| Error | Causa | Solución |
|-------|--------|-----------|
| `ModuleNotFoundError: PySide6` | No se instaló en el entorno virtual | Activa el venv y reinstala con `pip install PySide6` |
| El intérprete no coincide | VS Code usa otro Python | Selecciona el intérprete correcto (`Ctrl+Shift+P` → “Python: Select Interpreter”) |
| La app no se abre | Falta `app.exec()` | Asegúrate de incluirlo en `main.py` |
| Error de ruta al ejecutar | Estás en el directorio incorrecto | Entra en `src/` antes de ejecutar el script |

---

## Cierre y siguientes pasos

### Añadir un botón con señal y ranura

```python
from PySide6.QtWidgets import QPushButton

boton = QPushButton("Haz clic", self)
boton.move(150, 120)
boton.clicked.connect(lambda: print("Botón presionado"))
```

**Señales y ranuras:**  

- Una *señal* (signal) se emite cuando ocurre algo (clic, cambio, etc.).  
- Una *ranura* (slot) es la función que responde a esa señal.

### Usar un layout

En lugar de posiciones fijas (`move()`), puedes usar **layouts** (vertical, horizontal, grid) para adaptar automáticamente los elementos al tamaño de la ventana.

---

## Checklist rápido

- [x] venv creado y activado  
- [x] PySide6 instalado  
- [x] requirements.txt generado  
- [x] Código separado en `main.py` y `ventana.py`  
- [x] QApplication, widgets y ciclo de eventos explicados  
- [x] App probada y documentada

---

## 🧾 .gitignore recomendado

```bash
venv/
__pycache__/
*.pyc
.DS_Store
```

---

**Autor:** *Mario Asenjo*  
**Curso:** *Interfaces gráficas con Python (PySide6)*  
**Fecha:** *Octubre 2025*
