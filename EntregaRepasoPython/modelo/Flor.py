from Planta import ABCPlanta
from modelo.PlantaException import PlantaException

class Flor(ABCPlanta):
    def __init__(self, nombre:str = None, altura:float = None, precio:float = None, color:str = None):
        if color is None:
            raise PlantaException("No se pueden crear flores sin color.")
        if not isinstance(color, str):
            raise PlantaException("El atributo color debe ser de tipo cadena de texto.")
        super().__init__(nombre, altura, precio)
        self.color = color
    
    def getColor(self):
        return self.color
    
    def setColor(self, color:str):
        self.color = color

    def getDescripcion(self):
        return f"Flor {self.color} - Altura: {self.getAltura()} cm - Precio: {self.getPrecio()} €"
