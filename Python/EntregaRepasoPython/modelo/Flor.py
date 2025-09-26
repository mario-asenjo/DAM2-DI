from modelo.Planta import ABCPlanta
from modelo.PlantaException import PlantaException

class Flor(ABCPlanta):
    def __init__(self, nombre:str = None, altura:float = None, precio:float = None, color:str = None):
        try:
            self.validarColor(color)
        except PlantaException as e:
            raise PlantaException(f"Error al crear flor: {e}")
        super().__init__(nombre, altura, precio)
        self.color = color
    
    def getColor(self):
        return self.color
    
    def setColor(self, color:str):
        self.color = color

    def getDescripcion(self):
        return f"Flor {self.color} - Altura: {self.getAltura()} cm - Precio: {self.getPrecio()} €"

    def validarColor(self, color:str):
        if not color:
            raise PlantaException("El atributo color no puede estar vacío.")
        if not isinstance(color, str):
            raise PlantaException("El atributo color debe ser de tipo cadena de texto.")