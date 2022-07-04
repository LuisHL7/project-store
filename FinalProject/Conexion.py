# Paquetes Importados
from PyQt5 import QtWidgets, QtSql


# Clase que permite la conexión a la BD
class Conexion:

    # Función que conecta con la BD.
    def dbConnect(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(self))
        if not db.open():
            QtWidgets.QMessageBox.critical(None, "No se puede abrir la base de datos",
                                           'No se puede establecer conexión.\n'
                                           'Haz click para cancelar.',
                                           QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión establecida')
        return True
