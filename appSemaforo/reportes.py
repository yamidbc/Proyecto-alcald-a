from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Datos para la tabla
datos_tabla = [
    ['ID', 'Nombre', 'Descripción', 'Valor Actual', 'Meta Actual', 'Presupuesto', 'Estado'],
    # Agrega los datos de la tabla aquí
]

# Datos para los gráficos
datos_grafico_torta = [
    # Agrega los datos del gráfico de torta aquí
]

datos_grafico_linea = [
    # Agrega los datos del gráfico de línea aquí
]

def generar_reporte(request):
    # Crea el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Estilos para el PDF
    estilo_titulo = ParagraphStyle(name='titulo', fontSize=18, alignment=TA_CENTER)
    estilo_cuerpo = ParagraphStyle(name='cuerpo', fontSize=12, alignment=TA_LEFT)

    # Título del reporte
    titulo = Paragraph('Reporte de Productos', estilo_titulo)
    doc.build([titulo, Spacer(1, 1 * inch)])

    # Tabla del reporte
    tabla = Table(datos_tabla, style=TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    doc.build([tabla, Spacer(1, 1 * inch)])

    # Gráfico de torta
    grafico_torta = Paragraph('Gráfico de Torta', estilo_titulo)
    doc.build([grafico_torta, Spacer(1, 1 * inch)])
    # Agrega el gráfico de torta aquí

    # Gráfico de línea
    grafico_linea = Paragraph('Gráfico de Línea', estilo_titulo)
    doc.build([grafico_linea, Spacer(1, 1 * inch)])
    # Agrega el gráfico de línea aquí

    return response
