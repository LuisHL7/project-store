# Paquetes Importados
import easygui
import var
import sys
from datetime import datetime


# Función salir que muestra una ventana de diálogo al usuario con dos botones, preguntando si está seguro de salir de
# la aplicación o no.
def salir():
    try:
        var.dialogo_salir.show()
        if var.dialogo_salir.exec():
            sys.exit()
        else:
            var.dialogo_salir.hide()
    except Exception as error:
        print('Error al intentar salir de la ventana', error)


# Función que muestra la fecha y la hora actual en la barra de estado.
def horaActual(self):
    now = datetime.now()
    self.ventana_principal.statusBar.showMessage(str(now.strftime("%d/%m/%Y, %H:%M:%S")))


# Función que muestra la ventana de díálogo con un calendario para poder seleccionar la fecha
def abrirCalendario():
    try:
        var.dialogo_fecha.show()
    except Exception as error:
        print('Error al abrir el calendario: %s ' % str(error))


# Función que carga la fecha seleccionada en LineEdit.
def cargarFecha(self):
    try:
        data = ('{0}-{1}-{2}'.format(self.day(), self.month(), self.year()))
        var.fecha.setText(str(data))
        var.dialogo_fecha.hide()
    except Exception as error:
        print('Error cargar fecha: %s' % str(error))


# Función que permite abrir el explorador de archivos.
def abrirExplorador():
    file = easygui.fileopenbox()
