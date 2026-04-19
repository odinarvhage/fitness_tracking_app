import os
import streamlit as st
import pandas as pd

import constants

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

ip = os.getenv("DB_IP")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

connection = mysql.connector.connect(
    host=ip,
    user=user,
    password=password,
    database=database)

if not connection.is_connected:
    print("Error connecting to MySQL database.")
    print("Please check your credentials and you are connected to the NTNU vpn and try again.")
    quit(0)

#read_table assumes the table exists.
def read_table(name):
    query = f"SELECT * FROM {name}"
    cursor = connection.cursor()
    cursor.execute(query)
    print("Fetched table " + name)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    df = pd.DataFrame(rows, columns=columns)
    if "password" in df.columns:
        df = df.drop(columns=["password"])
    return df

def create_entry(table, values):
    pass

def get_insertable_columns(table_name, db_tables):
    columns = db_tables[table_name]
    AUTO_SKIP = {"user_id", "workout_id", "metric_id"}
    return [col for col in columns if col not in AUTO_SKIP]

@st.dialog("CREATE entry")
def make_entry_dialog():
    table_name = st.selectbox("Choose a table", list(constants.create_tables.keys()))
    data = {}
    for col in constants.create_tables[table_name]:
        data[col] = st.text_input(col)
    if st.button("Submit"):
        empty_fields = [col for col, val in data.items() if val.strip() == ""]

        if empty_fields:
            st.error(f"These fields cannot be empty: {', '.join(empty_fields)}")
        else:
            st.session_state["new_entry"] = {
                "data": data,
                "table_name": table_name,
            }
            st.rerun()
