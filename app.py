#1.Importing REQUIRED LIBRARIES

import pandas as pd
import pymongo as py
import mysql.connector as sql
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from streamlit.components.v1 import html
from itables import to_html_datatable

# 2.Setting up page configuration

st.set_page_config(page_title= "AirBNB Analysis | By M.Kobalan",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

#3.Home TAB

SELECT = option_menu(
    menu_title = None,
    options = ["Home","Explore Data","About Project"],
    # icons =["house","bar-chart","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "red","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},   
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})

if SELECT=='Home':
    st.image("seattle.jpg")

    col1,col2=st.columns( 2)
    with col1:
        components.html("""
                    <html><body"><h1 style="font-family:Neutro; font-size:60px">AIRBNB History</h1></body></html>""",)
        st.image("history.png")
    with col2:
        components.html("""
                    <html><body><h1 style="font-family:Neutro; font-size:60px"> How Airbnb Works </h1></body></html>""",)
        st.image("how_airbnb_works.png")
    col3,col4=st.columns(2 )
    
    with col3:
        components.html("""
                    <html><body"><h1 style="font-family:Neutro; font-size:60px">SWOT ANALYSIS OF AIRBNB </h1></body></html>""",)
        st.image("airbnb_swot.png")
    with col4:
        components.html("""
                    <html><body><h1 style="font-family:Neutro; font-size:60px">  PESTLE:</h1></body></html>""",)
        st.image("Pestle.png")

    col5,col6= st.columns(2 )

    with col5:
        components.html("""
                    <html><body"><h1 style="font-family:Neutro; font-size:60px">Milestone </h1></body></html>""",)
        st.image("milestone.jpg")
    with col6:
        components.html("""
                    <html><body><h1 style="font-family:Neutro; font-size:60px">  Revenue Model </h1></body></html>""",)
        st.image("revenue model.jpg")
        st.image("about2.png")
        st.image("business model.jpg")

#4. Explore  Tab
elif SELECT=='Explore Data':
        
    #Map Creation
    Col1,Col2=st.columns([2,2])
    with Col1:
        hide_streamlit_style = """ <html><body><h1 style="font-family:Product sans; font-size:40px"> Airbnb Analysis in Map view </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        df=pd.read_csv('Cleaned_Dataset.csv')
        hide_streamlit_style = """ <html><body><h1 style="font-family:Product sans; font-size:25px"> Select A Country: </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        
        Countries=df['country'].unique().tolist()
        Countries=sorted(Countries)
        Country1=st.selectbox('abc',Countries,label_visibility = 'hidden')
        df_Country=df[df['country']==Country1]
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Total No. oF Property Type in the {Country1} country: {df_Country.property_type.nunique()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Total No. oF Room Type in the {Country1} country: {df_Country.room_type.nunique()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Total No. oF Bed Type in the {Country1} country: {df_Country.bed_type.nunique()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Total No. oF Hosts in the {Country1} country: {df_Country.host_name.nunique()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Maximum Nights(in days)  in the {Country1} country: {df_Country['maximum_nights'].max()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_streamlit_style = f"""<html><body><h1 style="font-family:Product sans; font-size:20px">Minimum Nights(in days) in the {Country1} country: {df_Country['minimum_nights'].min()} </h1></body></html>"""
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        Button1=st.button("Submit")

    with Col2:
        df_map=df[df['country']==Country1]
        fig_4 = px.scatter_mapbox(df_map, lat='latitude', lon='longitude', size='accommodates',hover_data =[ 'property_type', 'room_type', 'bed_type','minimum_nights', 'maximum_nights'],
                        color_continuous_scale= "rainbow",hover_name='name',range_color=(0,34000), mapbox_style='carto-darkmatter',
                        zoom=10)
        fig_4.update_layout(width=1150,height=800)
        st.plotly_chart(fig_4)   

        df1=df[['name',
            'minimum_nights', 'maximum_nights', 'cancellation_policy',
            'accommodates', 'bedrooms', 'beds', 'number_of_reviews', 'bathrooms',
            'price', 'cleaning_fee', 'extra_people', 'guests_included',
            'review_scores','host_name','availability_30', 'availability_60',
            'availability_90', 'availability_365']].loc[(df['country']==Country1)].reset_index(drop=True)
        
    if Button1:

        df1=pd.read_excel('Cleaned_Data.xlsx')
        components.html("""<html><body"><h3 style="font-family:Product sans; font-size:40px"> Hotel Details in Table View</h3></body></html>""",)
        html(
            to_html_datatable(
                df1[['Name','Min_nights','Max_nights','Cancellation_policy','Accommodates','Bedrooms','Beds','Bathrooms','Cleaning_Fee','Extra_People','Guests_included','No._of_reviews','Review_Scores','Price']].loc[(df['country']==Country1)].reset_index(drop=True),
                maxBytes=0,
            ),
            height=660,
        )

        df2=pd.read_excel('Cleaned_Data.xlsx')
        components.html("""<html><body"><h1 style="font-family:Product sans; font-size:40px"> Host Details in Table View</h1></body></html>""",)

        html(
            to_html_datatable(
                df2[['Name','Host_name','Host_response_time','Host_neighbourhood','Host_response_rate','Host_identity_verified','Host_total_listings_count','Availability_30','Availability_60','Availability_90','Availability_365']].loc[(df['country']==Country1)].reset_index(drop=True),
                maxBytes=0,
            ),
            height=660,
            )
        

    df=pd.read_csv('Cleaned_Dataset.csv')
    col1,col2=st.columns(2 )
    col3,col4=st.columns(2 )
    col5,col6=st.columns(2 )
    with col1:
        mean_Prices=df.groupby('property_type')['price'].mean().reset_index()
        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 1.Mean Price based on Property Type</h1></body></html>""",)
        fig = px.bar(df, y='price', x='property_type',width=500,height=500)
        fig.update_layout(
        xaxis_title="Bedrooms",
        yaxis_title="Bed Type ($)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig)
    with col2:
        mean_Score=df.groupby('host_name')['review_scores'].sum().reset_index().sort_values(by='review_scores',ascending=False)
        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 2.Top 10 host name based on sum oF review Scores</h1></body></html>""",)
        fig = px.bar(mean_Score.head(10), x='host_name', y="review_scores",height=600,width=500)
        fig.update_layout(
        xaxis_title="Host Name",
        yaxis_title="Total Review Scores",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig)
    
    with col3:
        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 3.Country based on Price(%) </h1></body></html>""",)
        fig = px.pie(df, values='price', names='country',width=700,height=500)
        st.plotly_chart(fig)

    with col4:
        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 4.Bed Type and Bed rooms based on Country</h1></body></html>""",)
        fig = px.bar(df, x='bedrooms', y="bed_type",color='country',barmode='stack',width=700,height=500)
        fig.update_layout(
        xaxis_title="Bedrooms",
        yaxis_title="Bed Type ($)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig)

    with col5:
        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 5.Total No. oF Accomodates based on Countries and Reviews</h1></body></html>""",)
        fig = px.bar(df, x="accommodates", y="number_of_reviews",color='country',barmode='stack',width=700)
        fig.update_layout(
        xaxis_title="Accommodates",
        yaxis_title="No. oF reviews",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig)

    with col6:

        components.html("""<html><body"><h1 style="font-family:Neutro; font-size:40px"> 6.Host response rate and price based on Countries</h1></body></html>""",)
        fig = px.bar(df, x="cancellation_policy", y="host_response_rate",color='country',barmode='stack',width=700)
        fig.update_layout(
        xaxis_title="Host Response rate",
        yaxis_title="Price",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig)


#5.About this Project
elif SELECT=='About Project':
     
    col1,col2= st.columns(2 )
    with col1:
        hide_streamlit_style = """ <html> <body><h1 style="font-family:Product sans; color:blue;font-size:40px"> About this Project </h1>
        <p style="font-family:Product sans; font-size:20px">
        <b>Project_Title</b>: <br>Airbnb Analysis Using Streamlit and Plotly <br>
        <b>Technologies_Used</b> :<br> Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb, PowerBI or Tableau 
        <br>
        <b>Dataset: </ b>https://drive.google.com/file/d/1C7AilYDf2pA09Jy-5wYysvLwKC9_Fu9X/view?usp=sharing <br>
        <b>Domain </b> : Travel Industry, Property Management and Tourism <br>
        <b>Problem Statement:</b>: <br>This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends<br>
        <b>Author</b> : M.KOBALAN <br>
        <b>Linkedin</b> :https://www.linkedin.com/in/kobalan-m-106267227/
        </p>
        </body>  </html>  """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
