from modelo.Planta import ABCPlanta
from modelo.PlantaException import PlantaException

class Cactus(ABCPlanta):
    def __init__(self, nombre:str = None, altura:float = None, precio:float = None, tieneEspinas:bool = None):
        if tieneEspinas is None:
            raise PlantaException("No se pueden crear cactus sin información sobre si tiene espinas.")
        if not isinstance(tieneEspinas, bool):
            raise PlantaException("El atributo tieneEspinas debe ser de tipo booleano.")
        super().__init__(nombre, altura, precio)
        self.tieneEspinas = tieneEspinas

    def getTieneEspinas(self):
        return self.tieneEspinas

    def setTieneEspinas(self, tieneEspinas:bool):
        self.tieneEspinas = tieneEspinas

    def getDescripcion(self):
        espinas = "con" if self.tieneEspinas else "sin"
        return f"Cactus {espinas} espinas - Altura: {self.getAltura()} cm - Precio: {self.getPrecio()} €"
