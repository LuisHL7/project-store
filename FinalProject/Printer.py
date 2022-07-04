# Paquetes Importados
from datetime import datetime
from PyQt5 import QtSql
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import var


# Función que muestra todos los datos del reporte.
def reporteProducto():
    try:
        var.rep = canvas.Canvas('informes/listadoProductos.pdf', pagesize=A4)
        cabecera()
        var.rep.setFont('Helvetica-Bold', size=9)
        textListado = 'Lista de Productos'
        var.rep.drawString(255, 735, textListado)
        var.rep.line(45, 730, 525, 730)
        camposProductos = ['CODIGO', 'NOMBRE', 'CATEGORIA', 'CANTIDAD', 'PRECIO_VENTA']
        var.rep.drawString(45, 710, camposProductos[0])
        var.rep.drawString(90, 710, camposProductos[1])
        var.rep.drawString(180, 710, camposProductos[2])
        var.rep.drawString(325, 710, camposProductos[3])
        var.rep.drawString(465, 710, camposProductos[4])
        var.rep.line(45, 703, 525, 703)
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, nombre, categoria, cantidad, precio_venta from productos')
        var.rep.setFont('Helvetica', size=10)
        if query.exec_():
            i = 50
            j = 690
            while query.next():
                var.rep.drawString(i, j, str(query.value(0)))
                var.rep.drawString(i + 30, j, str(query.value(1)))
                var.rep.drawString(i + 130, j, str(query.value(2)))
                var.rep.drawString(i + 280, j, str(query.value(3)))
                var.rep.drawRightString(i + 470, j, str(query.value(4)))
                j = j - 30
        pie(textListado)
        var.rep.save()
        rootPath = ".\\informes"
        cont = 0
        for file in os.listdir(rootPath):
            if file.endswith('.pdf'):
                os.startfile("%s/%s" % (rootPath, file))
            cont = cont + 1
    except Exception as error:
        print('Error al crear el reporte %s' % str(error))


# Función que muestra la cabecera del reporte
def cabecera():
    try:
        logo = 'images/logote.png'
        var.rep.setTitle('INFORME DE LOS PRODUCTOS')
        var.rep.setAuthor('Luis Huapaya')
        var.rep.setFont('Helvetica', size=10)
        var.rep.line(45, 820, 525, 820)
        var.rep.line(45, 745, 525, 745)
        var.rep.drawString(50, 805, 'A28072018L')
        var.rep.drawString(50, 790, 'Proyecto Final S.A.C')
        var.rep.drawString(50, 775, 'Calle Roris 79 1 Izq.')
        var.rep.drawString(50, 760, '722496572')
        var.rep.drawImage(logo, 450, 752, mask='auto')
    except Exception as error:
        print('Error en la cabecera del informe %s' % str(error))


# Función que muestra el pie de página del reporte.
def pie(textListado):
    try:
        var.rep.line(50, 50, 525, 50)
        date = datetime.today()
        date = date.strftime('%d.%m.%Y %H.%M.%S')
        var.rep.setFont('Helvetica-Oblique', size=7)
        var.rep.drawString(460, 40, date)
        var.rep.drawString(275, 40, str('Página %s' % var.rep.getPageNumber()))
        var.rep.drawString(50, 40, str(textListado))
    except Exception as error:
        print('Error en el pie del informe %s' % str(error))
