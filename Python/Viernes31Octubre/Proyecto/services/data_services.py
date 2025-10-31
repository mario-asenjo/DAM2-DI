"""
CAPA DE SERVICIOS: PROPORCIONA DATOS EN FORMATO CSV PARA LA APLICACION
"""

"""
    SERVICIO QUE PROVEE DATOS EN FORMATO CSV
    ESTA CLASE SIMULA LA OBTENCIÓN DE DATOS DESDE UNA FUENTE EXTERNA (ARCHIVO, API, BBD, ETC)
 """
class DataService:

    """
        obtener_datos_combobox() -> str
        Obtiene datos para el combobox
        Params: self
        Returns:
            str: Datos con el formato para el combobox
    """
    # DEBE RECIBIR LOS DATOS EN VEZ DE HARDCODEARLOS
    def obtener_datos_combobox() -> str:
        
        datos = """OPCION 1
        OPCION 2
        OPCION 3
        OPCION 4
        OPCION 5"""
        return datos.strip()
    
    """
    
    obtener_datos_tabla() -> str
    Obtiene datos para la tabla
    Params: self
    Returns:
        str: Datos en formato CSV separados por comas y saltos de línea.
    """
    def obtener_datos_tabla(self):
        datos = """ID, NOMBRE, DESCRIPCION
        1, Producto 1, Descripcion producto 1
        2, Producto 2, Descripcion producto 2
        3, Producto 3, Descripcion producto 3"""
        return datos
    
    def obtener_datos_http(self) -> str:
        pokemons = list()

        