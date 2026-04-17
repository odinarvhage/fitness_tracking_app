import streamlit as st
import mysql.connector
import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="10.212.175.85",
    user="teamplayer",
    password="hawktuah1",
    database="playground")

st.set_page_config(
    page_title="Fitness Tracking App",
    layout="wide"
)


cursor = connection.cursor()
