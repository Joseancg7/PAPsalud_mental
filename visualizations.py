
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def ts_clustering(df: pd.DataFrame, y: str, title: str):


    fig=go.Figure((go.Scatter(x=df.index, y=df[y],
                            mode='lines', name= y, line_color='#ffe476')))

    fig2 = px.scatter(df, x=df.index, y=y, 
                    color='Clusters', symbol='Fecha_importante', 
                    labels={"Clusters": "Cluster", "Fecha_importante": 'Fecha_importante'},  hover_data=['Evento'])


    fig.add_traces(fig2.data)
  


    fig.update_layout(legend_title="Clusters", title=title)


    fig.show()

def clusters_fi(df: pd.DataFrame):

    data = df[df['Fecha_importante'] == 'Fecha importante']
    
    fig = px.scatter(data, x=data.Clusters, y=data.index, 
                    color='Clusters', hover_data=['Evento'], title='Clusters fechas importantes')


    fig.show()