from servicio.ViveroInterface import ViveroInterface
from modelo.Cactus import Cactus
from modelo.Flor import Flor

class ServicioVivero(ViveroInterface):
    def __init__(self):
        super().__init__()
        self.plantas = []
    
    def agregarCactus(self, nombre, altura, precio, tieneEspinas):
        cactus = Cactus(nombre, altura, precio, tieneEspinas)
        self.plantas.append(cactus)

    def agregarFlor(self, nombre, altura, precio, color):
        flor = Flor(nombre, altura, precio, color)
        self.plantas.append(flor)

    