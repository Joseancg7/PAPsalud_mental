

import pandas as pd
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.clustering import TimeSeriesKMeans, silhouette_score

def clean_data(df: pd.DataFrame, drop_col_index: str):

    data_c = df.dropna(subset=[drop_col_index])
    data_c.set_index(drop_col_index, inplace=True)
    data_c = data_c.fillna(method='ffill')

    return data_c

def optimum_clusters(df: pd.DataFrame, clusters: int):


    X_train = TimeSeriesScalerMeanVariance().fit_transform(df)
    # Initialize silhouette resultas
    silhouette = []

    # Get silhoutte for differente clusters
    for i in range(2,clusters):
        model = TimeSeriesKMeans(n_clusters=i, metric="dtw", max_iter=20).fit(X_train)
        labels = model.labels_
        silhouette.append(silhouette_score(X_train, labels, metric="dtw"))
    
    return silhouette, pd.DataFrame(silhouette).idxmax()

def clusters(df: pd.DataFrame, num_clusters):

    X_train = TimeSeriesScalerMeanVariance().fit_transform(df)
    model = TimeSeriesKMeans(n_clusters=num_clusters, metric="dtw", max_iter=20).fit(X_train)
    df['Clusters'] = model.labels_ 

    separate_df = {}
    for i in range(num_clusters):
        separate_df['cluster_'+ str(i)] = df[df['Clusters'] == i]

    return separate_df

def comportamiento_clusters(dict_clusters: dict):

    dict_comportamiento = {}

    

    for i in range(len(dict_clusters)):

        cluster = dict_clusters['cluster_' + str(i)]
        cluster['datedif'] = cluster.index.to_series().diff().dt.days
        saltos = cluster[cluster['datedif']>1]
        indice_saltos = saltos.index.to_list()
        
        index_pos = []

        for j in indice_saltos:
            index_pos.append(cluster.index.get_loc(j))

        cambios = []

        if len(index_pos) == 0:
            resta = (cluster.iloc[-1,0:-1] - cluster.iloc[0,0:-1]).to_list()

            result = [1 if k>0 else -1 if k<0 else 0 for k in resta]

            cambios.append(result)

            cambios_df = pd.DataFrame(cambios, columns=cluster.columns.to_list()[0:-1])
            summary_cambios = cambios_df.apply(pd.Series.value_counts)
            dict_comportamiento['cluster_' + str(i)] = summary_cambios
            

    # Intialize for
        for j in range(len(index_pos)):

        # substract last minus first to get change in variables
            resta = (cluster.iloc[index_pos[j],0:-1] - cluster.iloc[index_pos[j-1],0:-1]).to_list()

        # Assign change values according to 1, -1, 0
            result = [1 if k>0 else -1 if k<0 else 0 for k in resta]

            cambios.append(result)
        
        # if the first time jump is not in the second position 
            if index_pos[0] != 1 & j == 0:
                resta = (cluster.iloc[0,0:-1] - cluster.iloc[index_pos[j-1],0:-1]).to_list()

                # Assign change values according to 1, -1, 0
                result = [1 if k>0 else -1 if k<0 else 0 for k in resta]

                cambios.append(result)

            # if the last position is not the end of the dataframe
            if index_pos[-1] != len(cluster) & j == len(index_pos)-2:

                resta = (cluster.iloc[index_pos[j],0:-1] - cluster.iloc[-1,0:-1]).to_list()

                # Assign change values according to 1, -1, 0
                result = [1 if k>0 else -1 if k<0 else 0 for k in resta]

                cambios.append(result)

        cambios_df = pd.DataFrame(cambios, columns=cluster.columns.to_list()[0:-1])
        summary_cambios = cambios_df.apply(pd.Series.value_counts)
        dict_comportamiento['cluster_' + str(i)] = summary_cambios

    return dict_comportamiento


def graph_prep(df: pd.DataFrame, df_fechas: pd.DataFrame):

    df.Clusters = df.Clusters.astype(str)
    df_fechas['Fecha'] = pd.to_datetime(df_fechas['Fecha'], format="%d/%m/%Y")

    lista_fechas = df_fechas['Fecha'].to_list()
    lista_eventos = df_fechas['Evento'].to_list()

    columna_match = []
    descripcion = []

    for i in range(len(df)):
            if df.iloc[i].name in lista_fechas:
                indice = lista_fechas.index(df.iloc[i].name)
                columna_match.append('Fecha importante')
                descripcion.append(lista_eventos[indice])
            else:
                columna_match.append('-')
                descripcion.append('-')


    df['Fecha_importante'] = columna_match
    df['Evento'] = descripcion


def caracterizacion_clusters(dict_compor: dict, per_min: float):

    comportamiento_comun = {}

    for i in list(dict_compor.keys()):

        compor = dict_compor[i].drop('Clusters', axis=1)
        crit_min = round(compor.sum(axis=0)[0]*per_min)
        max_indice = compor.idxmax()
        data = compor.max() >= crit_min
        resultado = pd.DataFrame()
        resultado['Variables'] = [data.index[i] for i in range(len(data)) if data[i]]
        resultado['Direcci??n'] = [max_indice[i] for i in range(len(data)) if data[i]]
        comportamiento_comun[i] = resultado

    return comportamiento_comun

def display_result(i: int, dict_comunes: dict):
    print('Comportamiento com??n cluster' + str(i+1) +' 80%:')
    display(dict_comunes['cluster_'+str(i)])



