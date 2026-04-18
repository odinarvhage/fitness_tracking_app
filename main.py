import sys

import streamlit as st

import tables

st.set_page_config(
    page_title="Fitness Tracking App",
    layout="wide"
)

st.title("Fitness Tracking App Demo - Group 5")
buttons = col1, col2, col3, col4 = st.columns(4)

with col1:
    health_button = st.button("Health")
with col2:
    goal_button = st.button("Goals")
with col3:
    user_button = st.button("User")
with col4:
    workout_button = st.button("Workout")

if health_button:
    health_frame = st.dataframe
    for key in tables.read_table("health_metric"):
        pass

if goal_button:
    pass

if user_button:
    pass

if workout_button:
    pass

if sys.argv.__len__() > 1:
    if sys.argv[1] == "status":
        tables.status_check()
