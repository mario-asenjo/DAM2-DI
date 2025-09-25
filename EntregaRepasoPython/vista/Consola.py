from colorama import Fore, Style, Back

def mostrarMensaje(mensaje):
    print(Fore.GREEN + mensaje + Style.RESET_ALL)

def mostrarError(mensaje):
    print(Fore.RED + mensaje + Style.RESET_ALL)