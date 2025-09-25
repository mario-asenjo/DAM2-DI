from modelo.PlantaException import PlantaException
from servicio.ServicioVivero import ServicioVivero
from vista import Consola

def iniciarControlador():
    vivero = ServicioVivero()
    
    try:
        vivero.agregarCactus("Cactus del desierto", 10.0, 15.0, True)
        Consola.mostrarMensaje("Planta añadida: Cactus del desierto.")

        vivero.agregarFlor("Rosa", 5.0, 10.0, "Rojo")
        Consola.mostrarMensaje("Planta añadida: Rosa.")

        vivero.agregarFlor("Tulipán", 7.0, 8.0, "Amarillo")
        vivero.agregarCactus("Mini cactus", 3.0, 5.0, False)
    except PlantaException as e:
        Consola.mostrarError(e.args[0])

    Consola.mostrarMensaje("\nListado de plantas registradas:")
    for planta in vivero.listarPlantas():
        Consola.mostrarMensaje(planta.getDescripcion()+ " - Altura: " + str(planta.getAltura()) + " cm - Precio: " + str(planta.getPrecio()) + " €")

    Consola.mostrarMensaje("\nPlantas con altura entre 30 y 50 cm:")
    for planta in vivero.buscarPorAlturaEntre(30, 50):
        Consola.mostrarMensaje(planta.getDescripcion())

    Consola.mostrarMensaje("\nPlantas con precio menor o igual a 6 €:")
    for planta in vivero.buscarPorPrecioMenorA(6):
        Consola.mostrarMensaje(planta.getDescripcion())

    try:
        eliminada = vivero.eliminarPrimeraPlantaConNombre("Rosa")
        Consola.mostrarMensaje(f"\nPlanta eliminada: {eliminada.getDescripcion()}")
    except PlantaException as e:
        Consola.mostrarError(e.args[0])

    buscada = vivero.buscarPlanta("Tulipán")
    Consola.mostrarMensaje(f"\nRegistro de busqueda de Tulipán: {buscada.getDescripcion() if buscada else "No encontrada."}")
    try:
        modificada = vivero.modificarPrecioPlanta("Cactus del desierto", 6.5)
        if modificada:
            Consola.mostrarMensaje(f"\nPrecio modificado: {modificada.getDescripcion()} - Nuevo precio: {modificada.getPrecio()} €")
        else:
            Consola.mostrarMensaje("\nNo se encontró la planta para modificar el precio.")
    except PlantaException as e:
        Consola.mostrarError(e.args[0])