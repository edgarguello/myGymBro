from vista.vista import VistaCLI
from controlador.controlador import Controlador

if __name__ == "__main__":
    vista = VistaCLI()
    controlador = Controlador(vista)
    controlador.iniciar()
