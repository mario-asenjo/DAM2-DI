from abc import ABC, abstractmethod
from modelo.PlantaException import PlantaException

class ABCPlanta(ABC):
    def __init__(self, nombre:str=None, altura:float=None, precio:float=None):
        try:
            self.validarNombre(nombre)
            self.validarAltura(altura)
            self.validarPrecio(precio)
        except PlantaException as e:
            raise PlantaException(f"Error al crear planta: {e}")
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

    def validarNombre(self, nombre:str):
        if not nombre:
            raise PlantaException("El nombre no puede estar vacío.")
        if not isinstance(nombre, str):
            raise PlantaException("El nombre debe ser una cadena de texto.")

    def validarAltura(self, altura:float):
            if not altura:
                raise PlantaException("La altura no puede estar vacía.")
            if not isinstance(altura, float):
                raise PlantaException("La altura debe ser un valor decimal.")
            if altura < 5.0 or altura > 300.0:
                raise PlantaException("La altura debe estar entre 5.0 y 300.0 cm.")
            
    def validarPrecio(self, precio:float):
            if not precio:
                raise PlantaException("El precio no puede estar vacío.")
            if not isinstance(precio, float):
                raise PlantaException("El precio debe ser un valor decimal.")
            if precio < 0.0:
                raise PlantaException("El precio debe ser mayor que 0.0 €.")