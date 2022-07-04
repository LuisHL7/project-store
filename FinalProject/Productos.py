# Paquetes Importados
import zipfile
import easygui
# import openpyxl
import win32api
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import Qt
import Eventos
import Printer
import var
from datetime import datetime
from main_form import Ui_MainWindowMain
import pandas as pd

# Clase que inicializa la ventana principal a la cual se accede después de introducir el usuario y contraseña correctos.
from windowsCalendarL import Ui_Dialog


class Iniciar(QtWidgets.QMainWindow):
    def __init__(self, nombre):
        super().__init__()
        self.ventana_principal = Ui_MainWindowMain()
        self.ventana_principal.setupUi(self)
        # Mensaje de Bienvenida con el nombre del usuario que ingresó.
        self.ventana_principal.LbWelcome.setText('Bienvenido, ' + nombre)
        self.ventana_principal.LbWelcome2.setText('Bienvenido, ' + nombre)
        # Cargar Datos
        self.cargarCampos()  # Cargando el QcomboBox
        self.cargarCategoria()
        self.cargarProveedor()
        Eventos.horaActual(self)  # Muestra la hora actual en la barra de estado
        self.mostrarProductos()  # Muestra los datos de la BD en el QTableWidget
        var.dialogo_fecha = Fecha()  # Asignando la clase Fecha a la variable global dialogo_fecha
        # Botones
        self.ventana_principal.CbSearch.currentTextChanged.connect(self.campoDeBusqueda)
        self.ventana_principal.BtnSearch.clicked.connect(self.campoDeConsulta)
        self.ventana_principal.BtnSearch_2.clicked.connect(self.buscarProducto)
        self.ventana_principal.BtnClean.clicked.connect(self.limpiarValores)
        self.ventana_principal.BtnClose.clicked.connect(Eventos.salir)
        self.ventana_principal.BtnCalendar.clicked.connect(Eventos.abrirCalendario)
        self.ventana_principal.BtnSave.clicked.connect(self.altaProductos)
        self.ventana_principal.BtnUpdate.clicked.connect(self.modificaProductos)
        self.ventana_principal.BtnDelete.clicked.connect(self.borrarProducto)
        # Barra de estado
        self.ventana_principal.actionOpen.triggered.connect(Eventos.abrirExplorador)
        self.ventana_principal.actionPrint.triggered.connect(Printer.reporteProducto)
        self.ventana_principal.actionImport.triggered.connect(self.importarDatos)
        self.ventana_principal.actionExport.triggered.connect(self.exportarBD)
        self.ventana_principal.actionCloseTB.triggered.connect(Eventos.salir)
        # Barra de menú
        self.ventana_principal.actionAbrir.triggered.connect(Eventos.abrirExplorador)
        self.ventana_principal.actionSalir.triggered.connect(Eventos.salir)

    # Función que de acuerdo a la opción que elijas en el QComboBox te mostrará un texto dentro del LineEdit.
    def campoDeBusqueda(self):
        self.ventana_principal.TxtCode.setText('')
        if self.ventana_principal.CbSearch.currentText() == "CODIGO":
            self.ventana_principal.TxtCode.setPlaceholderText("Ingrese el código")
        elif self.ventana_principal.CbSearch.currentText() == "NOMBRE":
            self.ventana_principal.TxtCode.setPlaceholderText("Ingrese el nombre")
        elif self.ventana_principal.CbSearch.currentText() == "CATEGORIA":
            self.ventana_principal.TxtCode.setPlaceholderText("Ingrese la categoría")
        elif self.ventana_principal.CbSearch.currentText() == "ESTADO":
            self.ventana_principal.TxtCode.setPlaceholderText("Ingrese el estado")
        elif self.ventana_principal.CbSearch.currentText() == "PROVEEDOR":
            self.ventana_principal.TxtCode.setPlaceholderText("Ingrese el proveedor")

    # Función que de acuerdo a la opción que elijas en el QComboBox te mostrará los datos obtenidos en el QTableWidget.
    def campoDeConsulta(self):
        if self.ventana_principal.CbSearch.currentText() == "CODIGO":
            self.buscarProductosPorCodigo()
        elif self.ventana_principal.CbSearch.currentText() == "NOMBRE":
            self.buscarProductosPorNombre()
        elif self.ventana_principal.CbSearch.currentText() == "CATEGORIA":
            self.buscarProductosPorCategoria()
        elif self.ventana_principal.CbSearch.currentText() == "ESTADO":
            self.buscarProductosPorEstado()
        elif self.ventana_principal.CbSearch.currentText() == "PROVEEDOR":
            self.buscarProductosPorProveedor()

    # Función que selecciona el estado y retorna el texto del radio button.
    def eligeEstado(self):
        estado = ""
        try:
            if self.ventana_principal.RbAvailable.isChecked():
                estado = 'DISPONIBLE'
            if self.ventana_principal.RbNotAvailable.isChecked():
                estado = 'NO DISPONIBLE'
            return estado
        except Exception as error:
            print('Error al seleccionar el estado:', error)

    # Cargar Datos
    # Función que carga los posibles campos dentro del QComboBox que se usarán para consultar la información
    def cargarCampos(self):
        try:
            campos = ['CODIGO', 'NOMBRE', 'CATEGORIA', 'ESTADO', 'PROVEEDOR']
            for i in campos:
                self.ventana_principal.CbSearch.addItem(i)
            self.ventana_principal.CbSearch.setCurrentIndex(-1)  # No muestra ningún valor inicial.
        except Exception as error:
            print('Error al cargar el QComboBox de los campos de búsqueda: %s ' % str(error))

    # Función que carga las categorías dentro del QComboBox.
    def cargarCategoria(self):
        try:
            campos = ['CEREALES', 'LEGUMBRES', 'VERDURAS', 'LECHE', 'PATATAS', 'DULCES', 'GALLETAS', 'LECHE']
            for i in campos:
                self.ventana_principal.CbCategory.addItem(i)
            self.ventana_principal.CbCategory.setCurrentIndex(-1)  # No muestra ningún valor inicial.
        except Exception as error:
            print('Error al cargar el QComboBox de las categorías: %s ' % str(error))

    # Función que carga los proveedores dentro del QComboBox.
    def cargarProveedor(self):
        try:
            campos = ['ALTEZA', 'GLORIA', 'LA HACIENDA', 'GALLO', 'NUTRIBÉN', 'COLA-CAO', 'NESTLE', 'GULLÓN',
                      'HACENDADO']
            for i in campos:
                self.ventana_principal.CbSupplier.addItem(i)
            self.ventana_principal.CbSupplier.setCurrentIndex(-1)  # No muestra ningún valor inicial.
        except Exception as error:
            print('Error al cargar el QComboBox de los proveedores: %s ' % str(error))

    # Operaciones CRUD PRODUCTOS
    # Consultas
    # Función que muestra en el QTableWidget todos los productos que hay en la BD.
    def mostrarProductos(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos')
        if query.exec_():
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos: ", query.lastError().text())

    # Función que busca por un código un determinado registro.
    def buscarProductosPorCodigo(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE codigo=:codigo')
        query.bindValue(':codigo', self.ventana_principal.TxtCode.text())
        if query.exec_():
            self.ventana_principal.cliTable.clearContents()
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos por código: ", query.lastError().text())

    # Función que consulta por como comienza el nombre o la totalidad del mismo y que devuelve el registro o los
    # registro que coincidan.
    def buscarProductosPorNombre(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE nombre LIKE :nombre')
        query.bindValue(':nombre', self.ventana_principal.TxtCode.text() + "%")
        if query.exec_():
            self.ventana_principal.cliTable.clearContents()
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos por nombre: ", query.lastError().text())

    # Función que consulta por como comienza la categoría o la totalidad del mismo y que devuelve el registro o los
    # registro que coincidan.
    def buscarProductosPorCategoria(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE categoria LIKE :categoria')
        query.bindValue(':categoria', self.ventana_principal.TxtCode.text() + "%")
        if query.exec_():
            self.ventana_principal.cliTable.clearContents()
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos por categoría: ", query.lastError().text())

    # Función que consulta por como comienza el estado o la totalidad del mismo y que devuelve el registro o los
    # registro que coincidan.
    def buscarProductosPorEstado(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE estado LIKE :estado')
        query.bindValue(':estado', self.ventana_principal.TxtCode.text() + "%")
        if query.exec_():
            self.ventana_principal.cliTable.clearContents()
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos por categoría: ", query.lastError().text())

    # Función que consulta por como comienza el nombre del proveedor o la totalidad del mismo y que devuelve el
    # registro o los registro que coincidan.
    def buscarProductosPorProveedor(self):
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE proveedor LIKE :proveedor')
        query.bindValue(':proveedor', self.ventana_principal.TxtCode.text() + "%")
        if query.exec_():
            self.ventana_principal.cliTable.clearContents()
            self.mostrarEnTabla(query)
        else:
            print("Error al mostrar los productos por categoría: ", query.lastError().text())

    # Función que se encarga de llenar el QTableWidget con los valores que se obtienen de la BD.
    def mostrarEnTabla(self, query):
        index = 0
        cont = 0
        while query.next():
            self.ventana_principal.cliTable.setRowCount(index + 1)
            self.ventana_principal.cliTable.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
            self.ventana_principal.cliTable.setItem(index, 1, QtWidgets.QTableWidgetItem(query.value(1)))
            self.ventana_principal.cliTable.setItem(index, 2, QtWidgets.QTableWidgetItem(query.value(2)))
            self.ventana_principal.cliTable.setItem(index, 3, QtWidgets.QTableWidgetItem(query.value(3)))
            self.ventana_principal.cliTable.setItem(index, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))
            self.ventana_principal.cliTable.setItem(index, 5, QtWidgets.QTableWidgetItem(str(query.value(5))))
            self.ventana_principal.cliTable.setItem(index, 6, QtWidgets.QTableWidgetItem(str(query.value(6))))
            self.ventana_principal.cliTable.setItem(index, 7, QtWidgets.QTableWidgetItem(query.value(7)))
            self.ventana_principal.cliTable.setItem(index, 8, QtWidgets.QTableWidgetItem(query.value(8)))
            index += 1
            cont += 1
        if cont == 0:
            win32api.MessageBox(0, "El valor ingresado no existe. Por favor, ingrese un valor existente.", "Error")

    # Función que busca un producto por su id y carga las cajas de texto con sus datos.
    def buscarProducto(self):
        cont = 0
        query = QtSql.QSqlQuery()
        query.prepare(
            'SELECT codigo, nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, estado, proveedor '
            'FROM productos WHERE codigo=:codigo')
        query.bindValue(':codigo', self.ventana_principal.TxtId.text())
        if query.exec_():
            while query.next():
                self.ventana_principal.TxtId.setText(str(query.value(0)))
                self.ventana_principal.TxtName.setText(query.value(1))
                self.ventana_principal.CbCategory.setCurrentText(str(query.value(2)).upper())
                self.ventana_principal.TxtDate.setText(str(query.value(3)))
                self.ventana_principal.TxtStock.setText(str(query.value(4)))
                self.ventana_principal.TxtPriceC.setText(str(query.value(5)))
                self.ventana_principal.TxtPriceV.setText(str(query.value(6)))
                if str(query.value(7)).upper() == 'DISPONIBLE':
                    self.ventana_principal.RbAvailable.setChecked(True)
                    self.ventana_principal.RbNotAvailable.setChecked(False)
                else:
                    self.ventana_principal.RbNotAvailable.setChecked(True)
                    self.ventana_principal.RbAvailable.setChecked(False)
                self.ventana_principal.CbSupplier.setCurrentText(str(query.value(8)).upper())
                cont += 1
            if cont == 0:
                win32api.MessageBox(0, "El código ingresado es incorrecto", "Error")
        else:
            print("Error al buscar un producto: ", query.lastError().text())

    # INSERTAR
    # Función que inserta los datos en la BD
    def altaProductos(self):
        try:
            self.insertarProducto(self.leerDatos())
            self.limpiarValores()
        except Exception as error:
            print('Error al insertar un producto: %s ' % str(error))

    # Función que ejecuta la sentencia en la BD para el registro un producto
    def insertarProducto(self, nuevoProducto):
        query = QtSql.QSqlQuery()
        query.prepare(
            "INSERT INTO productos (nombre, categoria, fecha_ingreso, cantidad, precio_costo, precio_venta, "
            "estado, proveedor) VALUES ( :nombre, :categoria, :fecha_ingreso, :cantidad, :precio_costo, "
            ":precio_venta, :estado, :proveedor)")
        self.cargarDatos(nuevoProducto, query)
        if query.exec_():
            self.mostrarProductos()
            self.ventana_principal.LbStatus.setText(
                'Producto con nombre ' + str(nuevoProducto[0]).lower() + ' ha sido insertado.')
        else:
            print("Error al insertar: ", query.lastError().text())

    # ACTUALIZAR
    # Función que actualiza los datos en la BD
    def modificaProductos(self):
        try:
            self.actualizaProductos(self.leerDatos())
            self.limpiarValores()
        except Exception as error:
            print('Error al actualizar un producto: %s ' % str(error))

    # Función que ejecuta la sentencia en la BD para actualizar un producto
    def actualizaProductos(self, productoModificado):
        query = QtSql.QSqlQuery()
        id = self.ventana_principal.TxtId.text()
        query.prepare(
            'UPDATE productos SET  nombre=:nombre, categoria=:categoria, fecha_ingreso=:fecha_ingreso,'
            ' cantidad=:cantidad, precio_costo=:precio_costo, precio_venta=:precio_venta, estado=:estado,'
            ' proveedor=:proveedor WHERE codigo=:codigo')
        query.bindValue(':codigo', int(id))
        self.cargarDatos(productoModificado, query)
        if query.exec_():
            self.mostrarProductos()
            self.ventana_principal.LbStatus.setText('Producto con nombre ' + str(productoModificado[0]).lower() +
                                                    ' ha sido actualizado.')
        else:
            print('Error al actualizar el producto ', query.lastError().text())

    # Función que recoge los valores de la caja de texto y los almacena en un array, para luego insertarlos en la BD
    def leerDatos(self):
        # Preparamos el registro
        var.estado = self.eligeEstado()
        nuevoProducto = [self.ventana_principal.TxtName.text().upper(), self.ventana_principal.CbCategory.currentText(),
                         self.ventana_principal.TxtDate.text(), self.ventana_principal.TxtStock.text(),
                         self.ventana_principal.TxtPriceC.text(), self.ventana_principal.TxtPriceV.text(),
                         var.estado, self.ventana_principal.CbSupplier.currentText()]
        return nuevoProducto

    # Función que guarda los datos que están almacenados en el array.
    def cargarDatos(self, nuevoProducto, query):
        query.bindValue(':nombre', str(nuevoProducto[0]))
        query.bindValue(':categoria', str(nuevoProducto[1]))
        query.bindValue(':fecha_ingreso', str(nuevoProducto[2]))
        query.bindValue(':cantidad', str(nuevoProducto[3]))
        query.bindValue(':precio_costo', str(nuevoProducto[4]))
        query.bindValue(':precio_venta', str(nuevoProducto[5]))
        query.bindValue(':estado', str(nuevoProducto[6]))
        query.bindValue(':proveedor', str(nuevoProducto[7]))

    # Eliminar
    # Función que recoge el código del producto y llama a la función eliminar producto
    # y después de ejecutarse se limpian los campos.
    def borrarProducto(self):
        try:
            self.eliminarProducto(self.ventana_principal.TxtId.text())
            self.limpiarValores()
        except Exception as error:
            print('Error al borrar un producto: %s ' % str(error))

    # Función que realiza la sentencia de eliminar un determinado producto.
    def eliminarProducto(self, codigo):
        query = QtSql.QSqlQuery()
        query.prepare('delete from productos where codigo =:codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            self.mostrarProductos()
            self.ventana_principal.LbStatus.setText('Producto con código ' + codigo + ' ha sido eliminado.')
        else:
            print("Error al eliminar el producto: ", query.lastError().text())

    # Función que limpia las cajas de texto.
    def limpiarValores(self):
        self.ventana_principal.TxtId.setText('')
        self.ventana_principal.TxtName.setText('')
        self.ventana_principal.TxtDate.setText('')
        self.ventana_principal.TxtStock.setText('')
        self.ventana_principal.TxtPriceC.setText('')
        self.ventana_principal.TxtPriceV.setText('')
        self.ventana_principal.CbCategory.setCurrentIndex(-1)
        self.ventana_principal.CbSupplier.setCurrentIndex(-1)
        self.ventana_principal.ButGroupStatus.setExclusive(False)
        self.ventana_principal.RbAvailable.setChecked(False)
        self.ventana_principal.RbNotAvailable.setChecked(False)

    #  Importar
    # Función que abre el explorador de archivos y seleccionando el archivo excel,
    # y llama a la función importarDatosDeExcel()
    def importarDatos(self):
        archivoExcel = easygui.fileopenbox()
        self.importarDatosDeExcel(archivoExcel)

    # Función que importa los datos del exel.
    # Nota: Se necesita instalar manualmente el openpyxl para funcionar.
    def importarDatosDeExcel(self, nombreArchivo):
        df = pd.read_excel(nombreArchivo)
        if df.size == 0:
            return print("El archivo está vació.")
        for row in df.itertuples():
            productoNuevo = [row.NOMBRE, row.CATEGORIA, str(datetime.date(row.FECHA_INGRESO))[:18], str(row.CANTIDAD),
                             str(row.PRECIO_COSTO), str(row.PRECIO_VENTA), row.ESTADO, row.PROVEEDOR]
            self.insertarProducto(productoNuevo)

    # Exportar
    # Función que abre el explorador de archivos y llama a la función exportarBDEnZip().
    def exportarBD(self):
        archivoBD = easygui.fileopenbox()
        self.exportarBDEnZip(archivoBD)

    # Función que exporta la bd en zip.
    def exportarBDEnZip(self, archivoBD):
        jungle_zip = zipfile.ZipFile(str(archivoBD) + '.zip', 'w')
        jungle_zip.write(str(archivoBD), compress_type=zipfile.ZIP_DEFLATED)
        self.ventana_principal.LbStatus.setText('Información: El archivo fue exportado en zip correctamente.')
        jungle_zip.close()


class Fecha(QtWidgets.QDialog):
    def __init__(self):
        super(Fecha, self).__init__()
        var.dialogo_fecha = Ui_Dialog()
        var.dialogo_fecha.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)  # elimina la barra
        self.setAttribute(Qt.WA_TranslucentBackground)  # transparente
        var.dialogo_fecha.venCalendar.setSelectedDate(
            QtCore.QDate(datetime.now().year, datetime.now().month, datetime.now().day))
        var.dialogo_fecha.venCalendar.clicked.connect(Eventos.cargarFecha)
