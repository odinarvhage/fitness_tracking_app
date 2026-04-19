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

user_frame = st.dataframe(tables.read_table("users"))
if health_button:
    health_frame = st.dataframe(tables.read_table("health_metric"))

if goal_button:
    goal_frame = st.dataframe(tables.read_table("goals"))

    sub_goals = col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        weight_frame = st.dataframe(tables.read_table("weight_goals"))
    with col2:
        running_frame = st.dataframe(tables.read_table("running_goals"))
    with col3:
        sleep_frame = st.dataframe(tables.read_table("sleep_goals"))
    with col4:
        strength_frame = st.dataframe(tables.read_table("strength_goals"))
    with col5:
        step_frame = st.dataframe(tables.read_table("steps_goals"))

if user_button:
    user_frame = st.dataframe(tables.read_table("users"))

if workout_button:
    workout_frame = st.dataframe(tables.read_table("workout"))
    sub_workouts = col1, col2 = st.columns(2)
    with col1:
        workout_entry_frame = st.dataframe(tables.read_table("workout_entries"))
    with col2:
        exercise_frame = st.dataframe(tables.read_table("exercises"))


if sys.argv.__len__() > 1:
    if sys.argv[1] == "status":
        tables.status_check()
