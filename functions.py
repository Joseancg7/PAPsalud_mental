

import pandas as pd
import numpy as np
import tslearn
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
        model = TimeSeriesKMeans(n_clusters=i, metric="dtw", max_iter=10).fit(X_train)
        labels = model.labels_
        silhouette.append(silhouette_score(X_train, labels, metric="dtw"))
    
    return silhouette
