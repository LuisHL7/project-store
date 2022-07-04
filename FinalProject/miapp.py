# Paquetes Importados
import sys
import win32api
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt
import Productos
import Eventos
import var
import Conexion
from windowsAviso import Ui_Aviso
from login import Ui_MainWindowLogin
import time


# Clase Principal
class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ventana_login = Ui_MainWindowLogin()
        self.ventana_login.setupUi(self)
        var.dialogo_salir = Salir()  # Asignando la clase Salir a la variable global dialogo_salir
        self.setWindowFlag(Qt.FramelessWindowHint)  # elimina barra
        self.setAttribute(Qt.WA_TranslucentBackground)  # transparente
        Conexion.Conexion.dbConnect('BDProductos.db')  # Conexión
        self.ventana_login.ButLogin.clicked.connect(self.iniciarSesion)
        self.ventana_login.ButClose.clicked.connect(Eventos.salir)

    # Función que comprueba que el usuario y contraseña ingresado sean correctos.
    # Si son correctos acceden a toda la información si no se mostrará una caja
    # de mensaje, solicitando que introduzca datos válidos.
    def iniciarSesion(self):
        query = QtSql.QSqlQuery()
        query.prepare('SELECT nombre, apellidos FROM empleados WHERE usuario =:usuario and password =:password')
        query.bindValue(':usuario', self.ventana_login.TxtUser.text().upper())
        query.bindValue(':password', self.ventana_login.TxtPassword.text().upper())
        if query.exec_():
            if query.next():
                nombre = str(query.value(0))
                nombre += " " + str(query.value(1))
                for i in range(0, 99):
                    time.sleep(0.02)
                    self.ventana_login.LineProgress.setValue(i)
                    self.ventana_login.LbLoad.setText('Cargando...')
                self.hide()
                var.ventana_principal = Productos.Iniciar(nombre)
                var.fecha = var.ventana_principal.ventana_principal.TxtDate
                var.ventana_principal.show()
            else:
                win32api.MessageBox(0, "El usuario o contraseña ingresada es incorrecto", "Error")

        else:
            print("Error de inicio de sesión: ", query.lastError().text())


#   Clase que muestra un diálogo con botones, cuando intentas cerrar la ventana actual
class Salir(QtWidgets.QDialog):
    def __init__(self):
        super(Salir, self).__init__()
        var.dialogo_salir = Ui_Aviso()
        var.dialogo_salir.setupUi(self)
        var.dialogo_salir.BtnBoxAvisoYes.clicked.connect(self.accept)
        var.dialogo_salir.BtnBoxAvisoNo.clicked.connect(self.reject)
        self.setWindowFlag(Qt.FramelessWindowHint)  # elimina la barra
        self.setAttribute(Qt.WA_TranslucentBackground)  # transparente


# Función que ejecuta la clase MiApp
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())
