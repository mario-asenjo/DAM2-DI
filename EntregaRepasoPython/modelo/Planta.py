from abc import ABC, abstractmethod
from modelo.PlantaException import PlantaException

class ABCPlanta(ABC):
    def __init__(self, nombre:str=None, altura:float=None, precio:float=None):
        if nombre is None or altura is None or precio is None:
            raise PlantaException("No se pueden crear plantas sin nombre, altura o precio.")
        if (not isinstance(nombre, str) or not isinstance(altura, float) or not isinstance(precio, float)):
            raise PlantaException("No se pueden crear plantas con tipos de datos incorrectos.")
        super().__init__()
        self.nombre = nombre
        self.altura = altura
        self.precio = precio

    def getNombre(self):
        return (self.nombre)

    def getAltura(self):
        return (self.altura)
    
    def getPrecio(self):
        return (self.precio)

    def setNombre(self, nombre:str):
        self.nombre = nombre

    def setAltura(self, altura:float):
        self.validarAltura(altura)
        self.altura = altura
    
    def setPrecio(self, precio:float):
        self.validarPrecio(precio)
        self.precio = precio

    def getDescripcion(self):
        pass

    def validarAltura(altura:float):
            if not isinstance(altura, float):
                raise PlantaException("La altura debe ser un valor decimal.")
            if altura < 5.0 or altura > 300.0:
                raise PlantaException("La altura debe estar entre 5.0 y 300.0 cm.")
            
    def validarPrecio(precio:float):
            if not isinstance(precio, float):
                raise PlantaException("El precio debe ser un valor decimal.")
            if precio < 0.0:
                raise PlantaException("El precio debe ser mayor que 0.0 €.")