import uuid
import os
from datetime import datetime

def generate_unique_filename(filename):
    extension = os.path.splitext(filename)[1]
    unique_filename = str(uuid.uuid4()) + extension
    return unique_filename

def calcular_meses(vigencia):
    meses = []
    for mes in range(1, 13):
        fecha = datetime(vigencia, mes, 1)
        meses.append(fecha)
    return meses