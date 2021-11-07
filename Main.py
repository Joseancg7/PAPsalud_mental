from numpy import mod
import pandas as pd
import tslearn
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.clustering import TimeSeriesKMeans, KShape, silhouette_score


# Import data
data_o = pd.read_excel('Data\\Archivo_1_Datos_TS.xlsx')

# Drop rows with missing dates

data_c = data_o.dropna(subset=['Fecha'])

data_c = data_c.fillna(method='ffill')

X_train = TimeSeriesScalerMeanVariance().fit_transform(data_c.drop('Fecha', axis=1))

silhouette = []

for i in range(1,10):
    model = TimeSeriesKMeans(n_clusters=i, metric="dtw", max_iter=10).fit(X_train)
    labels = model.labels_
    silhouette.append(silhouette_score(X_train, labels, metric="dtw") )
