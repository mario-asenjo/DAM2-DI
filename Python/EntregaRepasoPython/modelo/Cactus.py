from modelo.Planta import ABCPlanta
from modelo.PlantaException import PlantaException

class Cactus(ABCPlanta):
    def __init__(self, nombre:str = None, altura:float = None, precio:float = None, tieneEspinas:bool = None):
        try:
            self.validarTieneEspinas(tieneEspinas)
        except PlantaException as e:
            raise PlantaException(f"Error al crear cactus: {e}")
        super().__init__(nombre, altura, precio)
        self.tieneEspinas = tieneEspinas

    def getTieneEspinas(self):
        return self.tieneEspinas

    def setTieneEspinas(self, tieneEspinas:bool):
        self.tieneEspinas = tieneEspinas

    def getDescripcion(self):
        espinas = "con" if self.tieneEspinas else "sin"
        return f"Cactus {espinas} espinas - Altura: {self.getAltura()} cm - Precio: {self.getPrecio()} €"

    def validarTieneEspinas(self, tieneEspinas:bool):
        if not tieneEspinas:
            raise PlantaException("El atributo tieneEspinas no puede estar vacío.")
        if not isinstance(tieneEspinas, bool):
            raise PlantaException("El atributo tieneEspinas debe ser de tipo booleano.")
    