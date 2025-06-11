from vista.vista_grafica import VistaGrafica
from controlador.controlador import Controlador

if __name__ == "__main__":
    app = VistaGrafica()
    controlador = Controlador(app)
    app.set_controlador(controlador)
    app.mainloop()

    