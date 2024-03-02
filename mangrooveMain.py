import streamlit as st
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
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

with st.expander("Unit of measures"):
    st.text('Latitude and Longitude: Typically measured in degrees (°) for geographic coordinates. '
            '  \nElevation: Usually measured in meters (m) above sea level. '
            '  \nTemperature: Commonly measured in degrees Celsius (°C) or Kelvin (K). '
            '  \nPrecipitation: Often measured in millimeters (mm) or inches (in) of rainfall. '
            '  \nHumidity: Usually expressed as a percentage (%). '
            '  \nSunlight Exposure: This can vary depending on the context. It might be measured in lux, watt per square meter (W/m²), or another unit related to illuminance or irradiance. '
            '  \nSoil pH: pH is a dimensionless quantity representing the acidity or alkalinity of soil. '
            '  \nSalinity: Usually measured in parts per thousand (ppt) or practical salinity units (psu). '
            '  \nNitrogen, Phosphorus, Potassium: These are typically measured in parts per million (ppm) or milligrams per kilogram (mg/kg). '
            '  \nOrganic Matter: Often measured in percentage (%) or grams per kilogram (g/kg). '
            '  \nTidal Inundation: This might be expressed as a percentage of time or as a dimensionless ratio. '
            '  \nWater Depth: Usually measured in meters (m) or centimeters (cm). '
            '  \nSoil Moisture: Typically measured as a percentage (%) or in volumetric water content (cm³/cm³). '
            '  \nGrowth Rate: Depending on the context, this could be measured in units of length per unit of time (e.g., meters per year). '
            '  \nPlant Height: Usually measured in meters (m) or centimeters (cm).')

#osm mapbox plotting entire plant data
#scatter map breaks sometimes after re-render
#st.map(filteredDf,latitude='Latitude',longitude='Longitude',
#       use_container_width=True,size=100,zoom=None)
#temp comm saves = mapbox_style="open-street-map"
fig = px.scatter_mapbox(filteredDf, lat="Latitude", lon="Longitude", mapbox_style="carto-positron", 
                  color="Mangrove_Species", color_discrete_sequence=["forestgreen","lawngreen","limegreen"], 
                  size="Growth_Rate", size_max=15, zoom=9)
fig.update_layout(mapbox=dict(bearing=0, center=dict(lat=20,lon=42),pitch=0,zoom=9))
st.plotly_chart(fig, use_container_width=True, height=700)

#temp vs lat
fig = px.scatter(filteredDf, x="Latitude", y="Temperature", 
                color="Mangrove_Species", color_discrete_sequence=["rgb(31, 119, 180)","rgb(255, 127, 14)","rgb(44, 160, 44)"],
                title="Latitude vs Temprature")
st.plotly_chart(fig, use_container_width=True,height=700)

#plant height and growth distribution distribution
fig = ff.create_distplot([filteredDf['Growth_Rate'],filteredDf['Plant_Height']], ['Growth Rate', 'Plant Height'], 
                         curve_type='kde')
fig.update_layout(title='Growth against plant height') 
st.plotly_chart(fig, use_container_width=True)

# Scatter plot for Soil Moisture vs Salinity vs organic matter
fig = px.scatter_matrix(filteredDf, dimensions=["Salinity", "Organic_Matter", "Soil_Moisture"], 
                        color="Mangrove_Species", 
                        color_discrete_sequence=["rgb(31, 119, 180)","rgb(255, 127, 14)","rgb(44, 160, 44)"],
                        title="Soil Moisture vs Salinity vs Organic matter")
st.plotly_chart(fig, use_container_width=True,height=700)

# Calculate average plant height across different mangrove species
fig = px.box(filteredDf, x="Mangrove_Species", y="Plant_Height", 
             color="Mangrove_Species", points="all",
             title="Average plant height across different species", color_discrete_sequence=["forestgreen","lawngreen","limegreen"])
st.plotly_chart(fig, use_container_width=True)

#average growth rate
fig = px.box(filteredDf, x="Mangrove_Species", y="Growth_Rate", 
             color="Mangrove_Species", points="all",
             title="Average growth rates", color_discrete_sequence=["forestgreen","lawngreen","limegreen"])
st.plotly_chart(fig, use_container_width=True)

#soil moist vs precipitation
#fig = px.scatter(filteredDf, x="Soil_Moisture", y="Precipitation", color="Mangrove_Species", size ='Growth_Rate', color_continuous_scale=px.colors.sequential.Viridis)
fig = px.scatter(filteredDf, x="Soil_Moisture", y="Precipitation", 
                 color="Mangrove_Species", size ='Growth_Rate', color_discrete_sequence=["forestgreen","lawngreen","limegreen"],
                 title="Soil Moisture vs Precipitation")
st.plotly_chart(fig, use_container_width=True, height=700)

#join plot species vs humidity vs temp
#note this needs statsmodels to be installed
fig = px.scatter(filteredDf, x="Humidity", y="Temperature", color="Mangrove_Species", marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white")
st.plotly_chart(fig, use_container_width=True, height=700)

#sunlight vs latitude
fig = px.scatter(filteredDf, x="Latitude", y="Sunlight_Exposure", 
                 color="Elevation", color_continuous_scale="Oranges",
                 title="Latitude vs Sunlight")
st.plotly_chart(fig, use_container_width=True,height=700)

#tidal vs precipitation
fig = px.scatter(filteredDf, x="Tidal_Inundation", y="Precipitation", 
                 color="Soil_Moisture", size="Plant_Height", color_continuous_scale="bugn_r",
                 title="Tidal Inundation vs Precipitation")
st.plotly_chart(fig, use_container_width=True,height=700)

#soil moisture vs water depth
fig = px.scatter(filteredDf, x="Soil_Moisture", y="Water_Depth", 
                 color="Water_Depth", size="Plant_Height", color_continuous_scale="blues_r",
                 title="Soil Moisture vs Water Depth")
st.plotly_chart(fig, use_container_width=True,height=700)

#corelation matrix
fig = px.imshow(filteredDf.corr(numeric_only = True),labels=dict(color="Corelation"),
                color_continuous_scale=DEFAULT_HEATMAP_COLOR, text_auto=True, 
                title="Corelation matrix")
fig.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=18
    )
)
fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True,height=700)

# date vs temp
#having lot of load time issue, breaking page sometimes
#fig = px.line(filteredDf, x="Date", y="Temperature")
#st.plotly_chart(fig, use_container_width=True,height=700)

#could be better plot based on grouping
#threadFrame = filteredDf[['Region','Elevation','Temperature','Humidity','Sunlight_Exposure']].copy()
#fig = px.parallel_coordinates(threadFrame, labels={"Region": "Region",
#                  "Elevation": "Elevation", "Temperature": "Temperature",
#                  "Humidity": "Humidity", "Sunlight_Exposure": "Sunlight Exposure"}, color_continuous_scale="viridis_r")
#st.plotly_chart(fig, use_container_width=True,height=700)


################ ignore below codes for SNS ###################

#col1, col2 = st.columns((2))
#with col1:
#    #corelation using matplotlib
#    plt.xticks(rotation=DEFAULT_TEXT_ROTATION_DEGREES)
#    fig, ax = plt.subplots(figsize=(20,15))
#    sns.heatmap(filteredDf.corr(numeric_only = True), annot = True, cmap = DEFAULT_HEATMAP_COLOR, cbar = False, ax=ax)
#    #sns.heatmap(df.corr(numeric_only = True), annot = True, cbar = False, fmt=DEFAULT_FORMAT, cmap=DEFAULT_COLORMAP)
#    #fig.tight_layout()
#    st.write(fig, use_container_width=True,height=700)
#with col2:
#    fig = px.imshow(filteredDf.corr(numeric_only = True),labels=dict(color="Corelation"),
#                    color_continuous_scale=DEFAULT_HEATMAP_COLOR, text_auto=True, 
#                    title="Corelation matrix")
#    fig.update_layout(
#        font=dict(
#            #family="Courier New, monospace",
#            size=18
#        )
#    )
#    fig.update_layout(height=700)
#    st.plotly_chart(fig, use_container_width=True,height=700)

#col11, col22 = st.columns((2))
#with col11:
#    fig, ax = plt.subplots(figsize=(20,15))
#    sns.scatterplot(data = filteredDf, x = 'Latitude', y ='Temperature', hue ='Mangrove_Species')
#    st.write(fig, use_container_width=True)
#with col22:
#    fig = px.scatter(filteredDf, x="Latitude", y="Temperature", 
#                     color="Mangrove_Species",color_continuous_scale="Viridis",
#                     title="Latitude vs Temprature")
#    st.plotly_chart(fig, use_container_width=True,height=700)

#density vs temp -- no density column found in DF
#fig = px.line(filteredDf, x="Temperature", y="Density", 
#              title="Temperature vs Density", color='Mangrove_Species')
#st.plotly_chart(fig, use_container_width=True, height=700)

#precipitation vs temp
#fig, ax = plt.subplots(figsize=(20,15))
#sns.kdeplot(data = filteredDf, x ='Temperature', hue ='Mangrove_Species')
#st.write(fig, use_container_width=True)

#precipitation vs humidity
#fig, ax = plt.subplots(figsize=(20,15))
#sns.jointplot(data = filteredDf, x ='Humidity', y='Temperature', hue ='Mangrove_Species')
#st.write(fig, use_container_width=True)

# Scatter plot for Soil Moisture vs Salinity
#fig, ax = plt.subplots(figsize=(20,15))
#plt.scatter(filteredDf['Soil_Moisture'], filteredDf['Salinity'], alpha=0.5,color = 'lightcoral')
#plt.title('Soil Moisture vs Salinity')
#plt.xlabel('Soil Moisture')
#plt.ylabel('Salinity')
#plt.grid(True,alpha = 0.5)
#st.write(fig, use_container_width=True)

# Scatter plot for Soil Moisture vs Organic Matter
#fig, ax = plt.subplots(figsize=(20,15))
#plt.scatter(filteredDf['Soil_Moisture'], filteredDf['Organic_Matter'], alpha=0.5,color = 'crimson')
#plt.title('Soil Moisture vs Organic Matter')
#plt.xlabel('Soil Moisture')
#plt.ylabel('Organic Matter')
#plt.grid(True,alpha = 0.5)
#st.write(fig, use_container_width=True)

#plant height distribution
#fig, ax = plt.subplots(figsize=(20,15))
#sns.histplot(data = filteredDf, x = 'Plant_Height',kde = True, color = 'gray')
#plt.title('Plant height distribution')
#plt.xlabel('Plant heights')
#st.write(fig, use_container_width=True)

################ ignore above codes ends for SNS ###################