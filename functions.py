

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

        for i in indice_saltos:
            index_pos.append(cluster.index.get_loc(i))


        cambios = []

    # Intialize for
        for i in range(len(index_pos)-1):

        # substract last minus first to get change in variables
            resta = (cluster.iloc[index_pos[i+1],0:-1] - cluster.iloc[index_pos[i],0:-1]).to_list()

        # Assign change values according to 1, -1, 0
            result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

            cambios.append(result)
        
        # if the first time jump is not in the second position 
            if index_pos[0] != 1 & i == 0:
                resta = (cluster.iloc[0,0:-1] - cluster.iloc[index_pos[i],0:-1]).to_list()

                # Assign change values according to 1, -1, 0
                result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

                cambios.append(result)

            # if the last position is not the end of the dataframe
            if index_pos[-1] != len(cluster) & i == len(index_pos)-2:

                resta = (cluster.iloc[index_pos[i+1],0:-1] - cluster.iloc[-1,0:-1]).to_list()

                # Assign change values according to 1, -1, 0
                result = [1 if j>0 else -1 if j<0 else 0 for j in resta]

                cambios.append(result)

        cambios_df = pd.DataFrame(cambios, columns=cluster.columns.to_list()[0:-1])
        summary_cambios = cambios_df.apply(pd.Series.value_counts)
        dict_comportamiento['cluster_' + str(i)] = summary_cambios


 

    return dict_comportamiento


def graph_prep(df: pd.DataFrame, df_fechas: pd.DataFrame):

    df.Clusters = df.Clusters.astype(str)
    df_fechas['Fecha'] = pd.to_datetime(df_fechas['Fecha'], format="%d/%m/%Y")

    columna_match = []

    for i in range(len(df)):
            if df.iloc[i].name in df_fechas['Fecha'].to_list():
                columna_match.append('Fecha importante')
            else:
                columna_match.append('-')


    df['Fecha_importante'] = columna_match


