import functions as fn
import data as dt


# Importar datos
data_o = dt.data_o

# Eliminar filas con fechas faltantes y rellenar datos faltantes
data_c = fn.clean_data(data_o, 'Fecha')

# Obtener datos para el óptimo número de clusters
silhouette = fn.optimum_clusters(data_c, 8)




# Build model with optimum number of clusters according to sihouette results
model = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10).fit(X_train)
etiquetas = model.labels_ 

# Analizar comportamiento de cada variable de cada cluster
# Analizar que subio/bajo/mantuvo y comaprar para que variables comparten este comportamiento en el cluster,
# Es decir comportamiento característico de cada cluster. 
# Una vez identificados los comportamientos carctarísticos de cada cluster indentificar 
# los eventos importantes, a qué cluster pertenecen y lo que esto dice de esos eventos. 

data_cluster = pd.DataFrame(data_c)
data_cluster['Cluster'] = etiquetas

# Split data by clusters
cluster_1 = data_cluster[data_cluster['Cluster']==0]

# Get date differences to identify time jumps
cluster_1['datedif'] = cluster_1.index.to_series().diff().dt.days

# Get postion of time jumpys
saltos = cluster_1[cluster_1['datedif']> 1]

# Get index of time jumps
lista_indice = saltos.index.to_list()

# For each index get location (optimize)
index_pos = []
for i in range(len(lista_indice)):
    pos = lista_indice[i]
    index_pos.append(cluster_1.index.get_loc(pos))

# Initilize lists for variable anlysis

cambios = []

# Intialize for
for i in range(len(index_pos)-1):

    # substract last minus first to get change in variables
    resta = (cluster_1.iloc[index_pos[i+1],0:-1] - cluster_1.iloc[index_pos[i],0:-1]).to_list()

    # Assign change values according to 1, -1, 0
    result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

    cambios.append(result)
    
    # if the first time jump is not in the second position 
    if index_pos[0] != 1 & i == 0:
        resta = (cluster_1.iloc[0,0:-1] - cluster_1.iloc[index_pos[i],0:-1]).to_list()

         # Assign change values according to 1, -1, 0
        result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

        cambios.append(result)

    # if the last position is not the end of the dataframe
    if lista_indice[-1] != len(cluster_1) & i == len(index_pos)-2:
        resta = (cluster_1.iloc[index_pos[i+1],0:-1] - cluster_1.iloc[-1,0:-1]).to_list()

         # Assign change values according to 1, -1, 0
        result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

        cambios.append(result)

cambios_df = pd.DataFrame(cambios, columns=cluster_1.columns.to_list()[0:-1])
summary_cambios = cambios_df.apply(pd.Series.value_counts)






cluster_2 = data_cluster[data_cluster['Cluster']==1]
cluster_2['datedif'] = cluster_2.index.to_series().diff()
diff_c2 = cluster_2[cluster_2.columns.to_list()[:-2]].diff()
diff_c2['datedif'] = cluster_2['datedif']
diff_c2.dropna(inplace=True)



cluster_3 = data_cluster[data_cluster['Cluster']==2]
cluster_3['datedif'] = cluster_3.index.to_series().diff()
diff_c3 = cluster_3[cluster_3.columns.to_list()[:-2]].diff()
diff_c3['datedif'] = cluster_3['datedif']
diff_c3.dropna(inplace=True)



