import pandas as pd
import tslearn

# Import data
data_o = pd.read_excel('Data\\Archivo_1_Datos_TS.xlsx')

# Drop rows with missing dates

data_c = data_o.dropna(subset=['Fecha'])

data_c = data_c.fillna(method='ffill')