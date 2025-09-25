from modelo.Planta import ABCPlanta

class ViveroInterface:
    def agregarCactus(self, nombre:str, altura:float, precio:float, tieneEspinas:bool) -> None:
        pass

    def agregarFlor(self, nombre:str, altura:float, precio:float, color:str) -> None:
        pass

    def buscarPlanta(self, nombre:str) -> ABCPlanta | None:
        pass

    def modificarPrecioPlanta(self, nombre:str, nuevoPrecio:float) -> ABCPlanta | None:
        pass

    def eliminarPrimeraPlantaConNombre(self, nombre:str) -> ABCPlanta | None:
        pass

    def listarPlantas(self) -> list[ABCPlanta]:
        pass

    def buscarPorAlturaEntre(self, minAltura:float, maxAltura:float) -> list[ABCPlanta]:
        pass

    def buscarPorPrecioMenorA(self, precio:float) -> list[ABCPlanta]:
        pass