from modelo.Planta import ABCPlanta
from modelo.PlantaException import PlantaException
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

    def buscarPlanta(self, nombre) -> ABCPlanta | None:
        for planta in self.plantas:
            if planta.nombre == nombre:
                return planta
        return None

    def modificarPrecioPlanta(self, nombre:str, nuevoPrecio:float) -> ABCPlanta | None:
        planta = self.buscarPlanta(nombre)
        if planta:
            try:
                planta.setPrecio(nuevoPrecio)
                return planta
            except PlantaException as e:
                raise e
        return None
    
    def eliminarPrimeraPlantaConNombre(self, nombre) -> ABCPlanta | None:
        planta = self.buscarPlanta(nombre)
        if planta:
            self.plantas.remove(planta)
            return planta
        else:
            raise PlantaException("No se encontró la planta con el nombre especificado.")

    def listarPlantas(self) -> list[ABCPlanta]:
        return self.plantas
    
    def buscarPorAlturaEntre(self, minAltura, maxAltura) -> list[ABCPlanta]:
        resultado = []
        for planta in self.plantas:
            if minAltura <= planta.altura <= maxAltura:
                resultado.append(planta)
        return resultado
    
    def buscarPorPrecioMenorA(self, precio) -> list[ABCPlanta]:
        resultado = []
        for planta in self.plantas:
            if planta.precio <= precio:
                resultado.append(planta)
        return resultado