
import pandas as pd

data_o = pd.read_excel('Data\\Archivo_1_Datos_TS.xlsx')

fechas = pd.read_excel('Data\\Fechas_importantes.xlsx')
fechas.columns = ['Fecha', 'Evento']