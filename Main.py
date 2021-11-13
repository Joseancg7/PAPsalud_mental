import functions as fn
import warnings
warnings.filterwarnings('ignore')
import data as dt


# Importar datos
data_o = dt.data_o

# Eliminar filas con fechas faltantes y rellenar datos faltantes
data_c = fn.clean_data(data_o, 'Fecha')

# Obtener datos para el óptimo número de clusters
silhouette, num_c = fn.optimum_clusters(data_c, 8)

# Build model with optimum number of clusters according to sihouette results
separate_clusters = fn.clusters(data_c, 3)

# Caracterización del cportamiento de cada cluster
comportamiento = fn.comportamiento_clusters(separate_clusters)

# Preparación para gráfica
fn.graph_prep(data_c, dt.fechas)

comunes = fn.caracterizacion_clusters(comportamiento, 0.80)



