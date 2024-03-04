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

#streamlit run .\mangroveMain.py --server.port 8501
#pipreqs path
#python -m pipreqs.pipreqs
#pip3 freeze > requirements.txt
#pip install -r requirements.txt 

URL = 'https://raw.githubusercontent.com/Dat-A-rtist/mangroveDashboard/main/synthetic_mangrove_dataset.csv'
logo_url = "resources/daLogo.jpg"
DEFAULT_COLORMAP = "coolwarm_r" #not needed
DEFAULT_FORMAT = '.0f' #not needed
DEFAULT_TEXT_ROTATION_DEGREES = 80
DEFAULT_HEATMAP_COLOR = 'viridis'

st.set_page_config(page_title="DatArtist Mangrove EDA", page_icon=":seedling:")
st.title(":seedling: Mangrove Analytics - Exploratory Data Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

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

st.sidebar.image(logo_url)
st.sidebar.header("Choose your filters")
#region
region = st.sidebar.multiselect("Pick your region", df["Region"].unique())
if not region:
    regionDf = df.copy()
else:
    regionDf = df[df["Region"].isin(region)]

#Mangrove_Species
species = st.sidebar.multiselect("Pick your mangrove species", df["Mangrove_Species"].unique())
if not species:
    filteredDf = regionDf.copy()
else:
    filteredDf = regionDf[regionDf["Mangrove_Species"].isin(species)] 

with st.expander(":sparkles: Welcome to the Mangrove Analytical Dashboard"):
    st.markdown("It's your gateway to exploring the height, moisture levels, species diversity, and growth rates within mangrove ecosystems through the power of Exploratory Data Analysis (EDA). "
            "  \nMangroves, with their unique adaptations, play a crucial role in coastal environments, influencing factors such as sea level rise resilience and biodiversity. "
            "  \nOur EDA approach dives deep into the data, providing insights into the varying heights of mangrove canopies, moisture content of soils, species distribution, and growth rates. "
            "  \nJoin us as we navigate through interactive visualizations and analyses, shedding light on the intricate relationships between these key parameters and facilitating informed decision-making for mangrove conservation and management")

with st.expander("Know your units!"):
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
fig.update_layout(title=dict(text="<b>Map plots of mangrove</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True, height=700)
''' Magroove trees, also known as mangroves, are vital ecosystems found along coastal areas. 
In Saudi Arabia, mangrove tree markers on maps typically indicate the presence of these unique habitats. 
Mangroves serve as crucial buffers against coastal erosion, provide habitats for diverse marine life, and offer protection against storm surges. 
These markers on maps signify areas where these ecosystems thrive, highlighting their significance for biodiversity conservation and coastal management in the Kingdom of Saudi Arabia.'''

#temp vs lat
fig = px.scatter(filteredDf, x="Latitude", y="Temperature", 
                color="Mangrove_Species", color_discrete_sequence=["rgb(31, 119, 180)","rgb(255, 127, 14)","rgb(44, 160, 44)"])
fig.update_layout(title=dict(text="<b>Latitude vs Temprature</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True,height=700)
'''Latitude dictates the geographical range of mangroves, thriving within 25 degrees north to 25 degrees south of the equator. 
Temperature influences their growth and distribution, with warm climates being favorable, but frost and extreme heat can be detrimental to mangrove health.'''

#plant height and growth distribution distribution
fig = ff.create_distplot([filteredDf['Growth_Rate'],filteredDf['Plant_Height']], ['Growth Rate', 'Plant Height'], 
                         curve_type='kde')
fig.update_layout(title=dict(text="<b>Growth against plant height</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16) 
st.plotly_chart(fig, use_container_width=True)
'''The growth range of a plant typically corresponds to its optimal environmental conditions for growth, including factors like temperature, soil type, and sunlight exposure. 
Plant height, on the other hand, varies depending on genetic traits, species, and environmental factors, often with taller plants requiring more space and resources to thrive. 
Balancing these factors ensures successful cultivation and healthy development of plants in a given environment.'''

# Scatter plot for Soil Moisture vs Salinity vs organic matter
fig = px.scatter_matrix(filteredDf, dimensions=["Salinity", "Organic_Matter", "Soil_Moisture"], 
                        color="Mangrove_Species", 
                        color_discrete_sequence=["rgb(31, 119, 180)","rgb(255, 127, 14)","rgb(44, 160, 44)"])
fig.update_layout(title=dict(text="<b>Soil Moisture vs Salinity vs Organic matter</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16) 
st.plotly_chart(fig, use_container_width=True,height=700)
'''A scatter plot illustrating soil moisture, salinity, and organic matter provides a visual representation of their relationship in a given area. 
Each point on the plot represents a specific soil sample, showing how moisture levels, salinity, and organic matter content vary across the sample set. 
Analyzing this plot can reveal correlations, patterns, or potential trends between these important soil properties, aiding in agricultural or environmental assessments and decision-making processes.'''

# Calculate average plant height across different mangrove species
fig = px.box(filteredDf, x="Mangrove_Species", y="Plant_Height", 
             color="Mangrove_Species", points="all", color_discrete_sequence=["forestgreen","lawngreen","limegreen"])
fig.update_layout(title=dict(text="<b>Average plant height across different species</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True)
'''A graph representing mangrove tree height illustrates the vertical growth pattern of these unique coastal trees over time or across different environmental conditions.'''

#average growth rate
fig = px.box(filteredDf, x="Mangrove_Species", y="Growth_Rate", 
             color="Mangrove_Species", points="all",
             color_discrete_sequence=["forestgreen","lawngreen","limegreen"])
fig.update_layout(title=dict(text="<b>Average growth rates</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True)
'''A graph representing the growth rate of mangrove trees demonstrates the speed of their vertical development over time, providing insights into their dynamic growth patterns in various habitats.'''

#soil moist vs precipitation
#fig = px.scatter(filteredDf, x="Soil_Moisture", y="Precipitation", color="Mangrove_Species", size ='Growth_Rate', color_continuous_scale=px.colors.sequential.Viridis)
fig = px.scatter(filteredDf, x="Soil_Moisture", y="Precipitation", 
                 color="Mangrove_Species", size ='Growth_Rate', color_discrete_sequence=["forestgreen","lawngreen","limegreen"])
fig.update_layout(title=dict(text="<b>Soil Moisture vs Precipitation</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True, height=700)
'''A graph depicting soil moisture versus precipitation for mangrove trees showcases the correlation between rainfall levels and soil moisture content in their habitats, 
offering insights into the ecological relationship between precipitation patterns and the water availability crucial for mangrove growth and survival.'''

#join plot species vs humidity vs temp
#note this needs statsmodels to be installed
#fig = px.scatter(filteredDf, x="Humidity", y="Temperature", color="Mangrove_Species", marginal_y="violin",
#           marginal_x="box", trendline="ols", template="simple_white")
fig = px.scatter(filteredDf, x="Humidity", y="Temperature", color="Mangrove_Species", 
                trendline="ols", template="simple_white")
fig.update_layout(title=dict(text="<b>Humidity Vs Temperature</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16) 
st.plotly_chart(fig, use_container_width=True, height=700)
'''The relationship between humidity and temperature for mangrove trees reflects their adaptation to specific coastal climates, highlighting how these factors influence their physiological processes and distribution in their natural habitats.'''

#sunlight vs latitude
fig = px.scatter(filteredDf, x="Latitude", y="Sunlight_Exposure", 
                 color="Elevation", color_continuous_scale="Oranges")
fig.update_layout(title=dict(text="<b>Latitude vs Sunlight</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True,height=700)
'''A graph plotting latitude against sunlight exposure for mangrove trees demonstrates how their distribution varies with changing latitudes, revealing patterns of sunlight availability crucial for their growth and ecological niche adaptation along region of Kingdom of Saudi Arabia'''

#tidal vs precipitation
fig = px.scatter(filteredDf, x="Tidal_Inundation", y="Precipitation", 
                 color="Soil_Moisture", size="Plant_Height", color_continuous_scale="bugn_r")
fig.update_layout(title=dict(text="<b>Tidal Inundation vs Precipitation</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True,height=700)
'''A graph depicting the relationship between tidal variation and precipitation for mangrove trees reveals how these environmental factors interact to shape the hydrological conditions crucial for the growth and resilience of mangrove ecosystems'''

#soil moisture vs water depth
fig = px.scatter(filteredDf, x="Soil_Moisture", y="Water_Depth", 
                 color="Water_Depth", size="Plant_Height", color_continuous_scale="blues_r")
fig.update_layout(title=dict(text="<b>Soil Moisture vs Water Depth</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
st.plotly_chart(fig, use_container_width=True,height=700)
'''Mangroves thrive in areas where soil moisture levels are consistently high, often correlating with shallow water depths. 
This symbiotic relationship ensures adequate water supply for root systems while also facilitating nutrient uptake. 
However, excessive water depth can lead to waterlogging, hindering oxygen availability to roots and impeding growth. 
Thus, an optimal balance between soil moisture and water depth is essential for the successful growth and sustainability of mangrove ecosystems.'''

#corelation matrix
fig = px.imshow(filteredDf.corr(numeric_only = True),labels=dict(color="Corelation"),
                color_continuous_scale=DEFAULT_HEATMAP_COLOR, text_auto=True)
fig.update_layout(title=dict(text="<b>Corelation matrix</b>"), title_x=0.4, title_font_color="yellow", title_font_size=16)
fig.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=18
    )
)
fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True,height=700)
'''A correlation matrix of mangrove data incorporates multiple factors to explore their interrelationships within the ecosystem. 
By analyzing correlations between variables such as soil moisture, salinity, temperature, precipitation, sunlight exposure, and tidal variation, researchers can identify patterns and dependencies. 
Strong positive correlations suggest variables that tend to increase or decrease together, indicating potential cause-effect relationships or shared environmental influences. 
Conversely, negative correlations imply variables that change in opposite directions. 
Understanding these correlations helps unveil the complex dynamics shaping mangrove ecosystems, aiding in conservation efforts and sustainable management strategies.'''

st.text('')
st.text('')
st.markdown(
    '`Create by` <a href="mailto:contact.datartist@gmail.com">Datartist</a>', unsafe_allow_html=True)

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
