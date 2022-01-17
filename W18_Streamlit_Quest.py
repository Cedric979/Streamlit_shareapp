#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import streamlit as st
import plotly.express as px


#Changing the background with an image that has to be in the same folder
import base64
main_bg = "image_app.jpeg"
main_bg_ext = "jpeg"

side_bg = "image_app.jpeg"
side_bg_ext = "jpeg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        background-size: 100% 100%
    }}
   .sidebar.sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        background-size: 100% 100%
    }}
    </style>
    
    """,
    unsafe_allow_html=True
)

#Defining the title
st.title("Let's display some stats on cars by continent")

#Openning the DF
link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_full = pd.read_csv(link)

#Building the filtering continent list
continent_list = list(df_full['continent'].value_counts().keys())
continent_list.append('ALL')

#Building the year slider selection
year_list = list(df_full['year'].value_counts().keys())
year_list.append('ALL')

#Defining the selectbox
label1 = "please select the continent you would like to filter"
continent_choosen = st.selectbox(label1,continent_list)

#Asking the user the Price and the Range
# Add a slider to the sidebar:
year_slider = st.sidebar.slider('Reduce the year range if you want to reduce the scope',1971, 1983, (1971,1983))

#Define the validation button
if st.button("Get Cars's statisctics"):
    if continent_choosen != 'ALL':
        continent_condition = df_full['continent'] == continent_choosen
        df1 = df_full[continent_condition]
    else:
        df1 = df_full
    if year_slider != 'ALL':
        year_condition1 = df_full['year'] >= year_slider[0]
        year_condition2 = df_full['year'] <= year_slider[1]
        df2 = df1[year_condition1 & year_condition2]
    else:
        df2=df1
    st.write("You selected cars years between",year_slider,"from this/these continent",continent_choosen)
    st.write(df2)
    cars_heatmap = sns.heatmap(df2.corr(),cmap="YlGnBu", center=0)
    #MilesPerGallon
    cars_mpg = sns.histplot(data=df2,x='mpg')
    #MilesPerGallon
    cars_mpg = sns.histplot(data=df2,x='mpg')
    #CubeInches
    cars_cubeinches = sns.histplot(data=df2,x='cubicinches')
    #HorsePower
    cars_hp = sns.histplot(data=df2,x='hp')
    #Years
    cars_years = sns.histplot(data=df2,x='year')
    #Scatter hp & weightlbs
    sns.scatterplot(data=df2,x='hp',y='weightlbs')
    #Plotting
    st.write()
    with st.expander('Please expand to see the plot'):
        st.title("below the heatmap for the selected cars")
        st.pyplot(fig=cars_heatmap.figure,clear_figure=True)
        st.write()
    
    with st.expander('Please expand to see the plot'):
        import matplotlib.pyplot as plt
        import seaborn as sns
        st.title("Horse Power distribution")
        fig = plt.figure()
        sns.histplot(data=df2,x='hp')
        st.write(fig)

    with st.expander('Please expand to see the plot'):
        import plotly.express as px
        st.title("Time to 60 & Horse Power animated over the years grouped by continent scatter plot")
        fig = px.scatter(df2,
            x=df2["time-to-60"],
            y=df2["hp"],
            color="continent",
            animation_frame="year",
            range_x=[8,25], range_y=[46,230]
        )
        fig.update_layout(
            xaxis_title="Time to 60",
            yaxis_title="Horse Power",
        )

        st.write(fig)
        
    with st.expander('Please expand to see the plot'):
        import plotly.express as px
        st.title("Horse Power by year with continent grouping")
        fig = px.scatter(df2,
            x=df2["year"],
            y=df2["hp"],
            color="continent",
        )
        fig.update_layout(
            xaxis_title="year",
            yaxis_title="Horse Power",
        )

        st.write(fig)
if st.button("Last button to click"):
    st.write("Thank you for checking my streamlit app ;-), Hope you liked it!")
