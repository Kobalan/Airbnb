#1.Importing REQUIRED LIBRARIES

import pandas as pd
import pymongo as py
import mysql.connector as sql
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit.components.v1 as components


#2.SQL
database= sql.connect(host="localhost",user ="root",password ="kobalan",auth_plugin="mysql_native_password",database="airbnb")
Cursor=database.cursor()


# 3.Setting up page configuration

st.set_page_config(page_title= "AirBNB Analysis | By M.Kobalan",
                   layout= "wide",
                   initial_sidebar_state= "expanded")


#Main PAGE

#Map Creation

hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:40px"> Airbnb Analysis in Map view </h1></body></html>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


Col1,Col2=st.columns([1,3])

with Col1:
    Cursor.execute(f'SELECT Country,latitude,longitude FROM airbnb_analaysis ')
    df_map=pd.DataFrame(Cursor.fetchall(),columns=Cursor.column_names)
    Countries=df_map['Country'].unique().tolist()
    Countries=sorted(Countries)
    hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:25px"> Select A Country: </h1></body></html>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    Country=st.selectbox('',Countries)
    
df_map=df_map[df_map['Country']==Country]
st.map(df_map)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Country Wise BAR Chart
Col3,Col4=st.columns(2)

with Col3:
    Cursor.execute(f'SELECT Country,SUM(Price) as Price FROM airbnb_analaysis GROUP BY Country')
    df_Bar1=pd.DataFrame(Cursor.fetchall(),columns=Cursor.column_names)
    Country=df_Bar1['Country'].tolist()
    Price=df_Bar1['Price'].tolist()
    Price=[int(i) for i in Price]
    hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Country Wise Bar Chart </h1></body></html>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    fig1=go.Figure(data=[go.Bar( x=Country,y=Price, marker=dict(color='black'), orientation="v" ),
    ],
    layout=go.Layout(xaxis=dict(title="Country"),
                    yaxis=dict(title="Price"),
                    font=dict(family="Neutro", size=50,  color="RebeccaPurple", variant="small-caps",)                                          
    ))
    fig1.update_layout(barmode="stack")
    fig1.update_layout( width=800,height=600,)
    st.plotly_chart(fig1)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Col5,Col6=st.columns(2)
with Col5:
    Cursor.execute(f'SELECT DISTINCT(Country) FROM airbnb_analaysis')
    df=pd.DataFrame(Cursor.fetchall(),columns=Cursor.column_names)
    hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:25px"> Select A Country: </h1></body></html>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    Country=st.selectbox('',df['Country'])
    

#Property Wise Bar Chart
Col7,Col8=st.columns([4,2])
with Col7:
    Cursor.execute(f'SELECT Country,Property_type,SUM(Price) as Price,COUNT(Property_type) as Total_Property FROM airbnb_analaysis GROUP BY Country,Property_type')
    df_Bar2=pd.DataFrame(Cursor.fetchall(),columns=Cursor.column_names)
    df_Bar2=df_Bar2[df_Bar2['Country']==Country]
    property_Type=df_Bar2['Property_type'].tolist()
    Price=df_Bar2['Price'].tolist()
    Price=[int(i) for i in Price]

    hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Property Wise Bar Chart </h1></body></html>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    fig2=go.Figure(data=[go.Bar( x=property_Type,y=Price, marker=dict(color='orange'), orientation="v" ),
    ],
    layout=go.Layout(xaxis=dict(title="Property_Type"),
                    yaxis=dict(title="Price"),
                    font=dict(family="Neutro", size=50,  color="RebeccaPurple", variant="small-caps",)                                          
    ))
    fig2.update_layout(barmode="stack")
    fig2.update_layout( width=900,height=600,)
    st.plotly_chart(fig2)


# Pie CHart
    hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Property Wise Pie Chart </h1></body></html>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    fig = px.pie(df_Bar2, names=property_Type, values=Price, hole=0.5)

    st.plotly_chart(fig, use_container_width=True)

#Room Type Bar Chart
with Col8:

        Cursor.execute(f'SELECT Country,Room_type,count(Room_type) AS Total FROM airbnb_analaysis group by country,room_type')
        df_Bar3=pd.DataFrame(Cursor.fetchall(),columns=Cursor.column_names)
        df_Bar3=df_Bar3[df_Bar3['Country']==Country]
        Room_type=df_Bar3['Room_type'].tolist()
        Total=df_Bar3['Total'].tolist()
        Total=[int(i) for i in Total]
        
        hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Room Wise Bar Chart </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        fig3=go.Figure(data=[go.Bar( x=Room_type,y=Total, marker=dict(color='blue'), orientation="v" ),
        ],
        layout=go.Layout(xaxis=dict(title="Room_type"),
                        yaxis=dict(title="Total_Number"),
                        font=dict(family="Neutro", size=50,  color="RebeccaPurple", variant="small-caps",)                                          
        ))
        fig3.update_layout(barmode="stack")
        fig3.update_layout( width=500,height=600,)
        st.plotly_chart(fig3)


# Pie CHart
        hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Room Wise Pie Chart </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        fig = px.pie(df_Bar3, names=Room_type, values=Total, hole=0.5)
        st.plotly_chart(fig, use_container_width=True)




#Table Wise Data

hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px"> Top 50 Hotel Details based on Price in Table Format: </h1></body></html>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df=pd.read_csv('AirBNB_Analysis.csv')

#Fetching the data and Store it on the DATAFRAME


df_1=df[["country","name","property_type","room_type","bed_type","cancellation_policy","minimum_nights","maximum_nights","accommodates","bedrooms","beds","number_of_reviews","bathrooms","price","extra_people","guests_included","review_scores"]]
# df_1.sort_values(by=['price'],ascending=False)
result1=df_1.iloc[:50].style.background_gradient(cmap="Oranges")
st.dataframe(result1)

hide_streamlit_style = """ <html><body><h1 style="font-family:Neutro; font-size:30px">Host Details in Table Format: </h1></body></html>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

df_3=df[["host_name","host_location","host_response_time","host_neighbourhood","host_response_rate","host_is_superhost","host_has_profile_pic","host_identity_verified","host_listings_count"]]
st.dataframe(df_3)
#About this Project

hide_streamlit_style = """ <html> <body><h1 style="font-family:Neutro; color:blue;font-size:40px"> About this Project </h1>
<p style="font-family:Neutro; font-size:20px">
<b>Project_Title</b>: <br>Airbnb Analysis Using Streamlit and Plotly <br>
<b>Technologies_Used</b> :<br> Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb, PowerBI or Tableau 
<br>
<b>Dataset: </b>https://drive.google.com/file/d/1C7AilYDf2pA09Jy-5wYysvLwKC9_Fu9X/view?usp=sharing <br>
<b>Domain </b> : Travel Industry, Property Management and Tourism <br>
<b>Problem Statement:</b>: <br>This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends<br>
<b>Author</b> : M.KOBALAN <br>
<b>Linkedin</b> :https://www.linkedin.com/in/kobalan-m-106267227/
</p>
</body>  </html>  """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)