import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

#Configuración y lectura del data set
st.set_page_config(layout="wide")
df=pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')


#limpieza del df
df2=df
df2=df2.dropna(subset=['Analysis Neighborhoods']) #quitar nulos
df2=df2.drop(['HSOC Zones as of 2018-06-05','OWED Public Spaces','Central Market/Tenderloin Boundary Polygon - Updated','Parks Alliance CPSI (27+TL sites)','ESNCAG - Boundary File','Supervisor District', 'point', 'SF Find Neighborhoods','Current Police Districts', 'Current Supervisor Districts'],axis=1) 
#quitar columnas sin uso para optimizar rendimiento


#Input de distrito
dis=df2['Police District'].unique()
district=st.selectbox('Selecciona el distrito policial', dis)
df2=df2[df2['Police District']==district]


#Títulos
st.title('Reportes de incidentes del departamento de policía desde 2018')
st.write('Distrito Policial: ',district)


#Registros
st.markdown("<h4 style= 'text-align: center ;color: #FA5858;'> Incidentes registrados</h4>", unsafe_allow_html=True)
st.dataframe(df2)


#Contenedores
MapaTabla= st.container()
BarrasPastelLineas=st.container()


#C1
with MapaTabla:
    col1,col2=st.columns(2)
    
    #MAPA de criminalidad
    mapa=pd.DataFrame()
    mapa['lat']=df2['Latitude']
    mapa['lon']=df2['Longitude']
    mapa=mapa.dropna()
    col1.markdown("<h4 style= 'text-align: center ;color: #FA5858;'>Mapa de incidentes registrados</h4>", unsafe_allow_html=True)
    col1.map(mapa)
    
    #TABLA de Crimenes
    num=df2['Incident Category'].value_counts()
    tabla=pd.DataFrame()
    tabla['Incident']=num.index
    t=[]
    for i in range(len(num)):
        t.append(num[i])
    tabla['Quantity']=t
    tabla=tabla.sort_values('Quantity',ascending=False)
    fig=go.Figure(data=go.Table(
            header=dict(values=list(tabla[['Incident','Quantity']].columns),
            fill_color='#FA5858',
            line_color='white'),
            cells=dict(values=[tabla.Incident,tabla.Quantity],
            fill_color='#F5A9A9',
            line_color='white')
        ))
    col2.markdown("<h4 style= 'text-align: center ;color: #FA5858;'>Tipos de Incidentes</h4>", unsafe_allow_html=True)
    col2.write(fig)


    
#C2

with BarrasPastelLineas:
    c1,c2,c3=st.columns(3)
#Barras 
    frec=df2.groupby('Incident Year')[['Analysis Neighborhoods']].count()
    fig1=go.Figure(data=[go.Bar(
    x=frec.index,
    y=frec['Analysis Neighborhoods'],
    marker_color='#FA5858')])
    fig1.update_layout(
        xaxis_title='Años',
        yaxis_title='Reportes')
    c1.markdown("<h4 style= 'text-align: center ;color: #FA5858;'> Reportes por año</h4>", unsafe_allow_html=True)
    c1.write(fig1)
    
    
    #Línea
    dia=df2['Incident Day of Week'].value_counts()
    pie_dia=pd.DataFrame()
    pie_dia['Incident Day of Week']=dia.index
    d=[]
    for i in range(len(dia)):
        d.append(dia[i])
    pie_dia['Total']=d
    fig2 = go.Figure(data=[go.Scatter(x = dia.index, y = pie_dia['Total'], marker_color='#FA5858')])
    fig2.update_layout(
        xaxis_title='Día de la semana',
        yaxis_title='Reportes')
    
    c2.markdown("<h4 style= 'text-align: center ;color: #FA5858;'>Reportes por día de la semana</h4>", unsafe_allow_html=True)
    c2.write(fig2)

    
    #Pastel
    res=df2['Resolution'].value_counts()
    graf=pd.DataFrame()
    graf['Resolution']=res.index
    r=[]
    for i in range(len(res)):
        r.append(res[i])
    graf['Total']=r
    fig3=go.Figure(data=[go.Pie(labels=graf['Resolution'], values=graf['Total'],hole=.5)])
    fig3.update_traces(marker=dict(colors=['#B40404','#FF0000','#FA5858','#F5A9A9','#F8E0E0']))
    c3.markdown("<h4 style= 'text-align: center ;color: #FA5858;'>Estado de resolución</h4>", unsafe_allow_html=True)
    c3.write(fig3)
    

