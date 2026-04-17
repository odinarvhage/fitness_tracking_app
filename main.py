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

if not connection.is_connected:
    print("Error connecting to MySQL database.")
    quit(0)

userTables = "User","Workout","WorkoutEntry","Exercise"
goalTables = "Goal","WeightGoal","SleepGoal","RunningGoal","StrengthGoal"
healthTables = "HealthMetric"

def read_table(name, conn):
    query = f"SELECT * FROM {name}"
    return pd.read_sql(query, conn)


healthButton = st.button("Health")
goalsButton = st.button("Goals")
userButton = st.button("User")

def initialize_webclient():
    pass

cursor = connection.cursor()
