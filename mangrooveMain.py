import streamlit as st
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import warnings
import plotly.figure_factory as ff
import importlib
from io import StringIO
if importlib.util.find_spec("pyodide") is not None:
    from pyodide.http import open_url
warnings.filterwarnings('ignore')

#streamlit run .\mangrooveMain.py --server.port 8501
#pipreqs path
#python -m pipreqs.pipreqs
#pip3 freeze > requirements.txt
#pip install -r requirements.txt 

st.set_page_config(page_title="DatArtist Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Mangroove EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

URL = 'https://raw.githubusercontent.com/Dat-A-rtist/mangrooveDashboard/main/synthetic_mangrove_dataset.csv'
DEFAULT_COLORMAP = "coolwarm_r" #not needed
DEFAULT_FORMAT = '.0f' #not needed
DEFAULT_TEXT_ROTATION_DEGREES = 80
DEFAULT_HEATMAP_COLOR = 'viridis'


# Define latitude and longitude ranges for each region
regions = [
    {"name": "Central", "latitude": (24.5, 27.0), "longitude": (34.5, 37.5)},  # Central region
    {"name": "Southern", "latitude": (16.5, 19.0), "longitude": (34.5, 37.5)},  # Southern region
    {"name": "Eastern", "latitude": (27.0, 29.5), "longitude": (37.5, 41.0)},  # Eastern region
    {"name": "Western", "latitude": (19.0, 21.5), "longitude": (41.0, 45.0)},  # Western region
    {"name": "Northern", "latitude": (21.5, 24.5), "longitude": (45.0, 48.5)}   # Northern region
]

# Function to determine the region based on latitude and longitude
def get_region(latitude, longitude):
    for region in regions:
        if region["latitude"][0] <= latitude <= region["latitude"][1] and \
           region["longitude"][0] <= longitude <= region["longitude"][1]:
            return region["name"]
    return "Unknown"

#needed for standalone streamlite version
#if importlib.util.find_spec("pyodide") is not None:
#    url_contents = open_url(URL)
#else:
#    r = requests.get(URL)
#    url_contents = StringIO(r.text)
#df = pd.read_csv(url_contents, encoding="ISO-8859-1")

df = pd.read_csv(URL, encoding="ISO-8859-1")
df['Date'] = pd.to_datetime(df['Date']) #clean datetime column
df["Region"] = df.apply(lambda row: get_region(row["Latitude"], row["Longitude"]), axis=1) #generate region

st.sidebar.header("Choose your filters")
#region
region = st.sidebar.multiselect("Pick your region", df["Region"].unique())
if not region:
    regionDf = df.copy()
else:
    regionDf = df[df["Region"].isin(region)]

#Mangrove_Species
species = st.sidebar.multiselect("Pick your mangroove species", df["Mangrove_Species"].unique())
if not species:
    filteredDf = regionDf.copy()
else:
    filteredDf = regionDf[regionDf["Mangrove_Species"].isin(species)]

col1, col2 = st.columns((2))

with col1:
    #corelation using matplotlib
    plt.xticks(rotation=DEFAULT_TEXT_ROTATION_DEGREES)
    fig, ax = plt.subplots(figsize=(20,15))
    sns.heatmap(filteredDf.corr(numeric_only = True), annot = True, cmap = DEFAULT_HEATMAP_COLOR, cbar = False, ax=ax)
    #sns.heatmap(df.corr(numeric_only = True), annot = True, cbar = False, fmt=DEFAULT_FORMAT, cmap=DEFAULT_COLORMAP)
    #fig.tight_layout()
    st.write(fig, use_container_width=True,height=700)
with col2:
    fig = px.imshow(filteredDf.corr(numeric_only = True),labels=dict(color="Corelation"),color_continuous_scale=DEFAULT_HEATMAP_COLOR)
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True,height=700)

#osm mapbox
st.map(filteredDf,latitude='Latitude',longitude='Longitude',use_container_width=True,size=100,zoom=None)

#temp vs lat
with col1:
    fig, ax = plt.subplots(figsize=(20,15))
    sns.scatterplot(data = filteredDf, x = 'Latitude', y ='Temperature', hue ='Mangrove_Species')
    st.write(fig, use_container_width=True)
with col2:
    fig = px.scatter(filteredDf, x="Latitude", y="Temperature", color="Mangrove_Species")
    st.plotly_chart(fig, use_container_width=True,height=700)

#precipitation vs temp
fig, ax = plt.subplots(figsize=(20,15))
sns.kdeplot(data = filteredDf, x ='Temperature', hue ='Mangrove_Species')
st.write(fig, use_container_width=True)

#precipitation vs humidity
fig, ax = plt.subplots(figsize=(20,15))
sns.jointplot(data = filteredDf, x ='Humidity', y='Temperature', hue ='Mangrove_Species')
st.write(fig, use_container_width=True)

# Scatter plot for Soil Moisture vs Salinity
fig, ax = plt.subplots(figsize=(20,15))
plt.scatter(df['Soil_Moisture'], df['Salinity'], alpha=0.5,color = 'lightcoral')
plt.title('Soil Moisture vs Salinity')
plt.xlabel('Soil Moisture')
plt.ylabel('Salinity')
plt.grid(True,alpha = 0.5)
st.write(fig, use_container_width=True)

# Scatter plot for Soil Moisture vs Organic Matter
fig, ax = plt.subplots(figsize=(20,15))
plt.scatter(df['Soil_Moisture'], df['Organic_Matter'], alpha=0.5,color = 'crimson')
plt.title('Soil Moisture vs Organic Matter')
plt.xlabel('Soil Moisture')
plt.ylabel('Organic Matter')
plt.grid(True,alpha = 0.5)
st.write(fig, use_container_width=True)
