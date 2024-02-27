import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
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