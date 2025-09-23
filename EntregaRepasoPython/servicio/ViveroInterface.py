from modelo.Planta import ABCPlanta
class ViveroInterface:
    def agregarCactus(nombre:str, altura:float, precio:float, tieneEspinas:bool) -> None:
        pass

    def agregarFlor(nombre:str, altura:float, precio:float, color:str) -> None:
        pass

    def buscarPlanta(nombre:str) -> ABCPlanta:
        pass

    def modificarPrecioPlanta(nombre:str, nuevoPrecio:float) -> ABCPlanta:
        pass

    def eliminarPrimeraPlantaConNombre(nombre:str) -> ABCPlanta:
        pass

    def listarPlantas() -> list[ABCPlanta]:
        pass

    def buscarPorAlturaEntre(minAltura:float, maxAltura:float) -> list[ABCPlanta]:
        pass

    def buscarPorPrecioMenorA(precio:float) -> list[ABCPlanta]:
        pass