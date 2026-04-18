from asyncio import all_tasks

import streamlit as st
import mysql.connector
import mysql.connector


import tables

connection = mysql.connector.connect(
    host="10.212.175.85",
    user="teamplayer",
    password="hawktuah1",
    database="playground")

st.set_page_config(
    page_title="Fitness Tracking App",
    layout="wide"
)


def table_exists(table_name, conn):
    query = """
       SELECT COUNT(*)
       FROM information_schema.tables
       WHERE table_schema = %s
         AND table_name = %s
       """
    cursor = conn.cursor()
    cursor.execute(query, (conn.database, table_name))
    exists = cursor.fetchone()[0] == 1
    cursor.close()
    return exists



if not connection.is_connected:
    print("Error connecting to MySQL database.")
    quit(0)

def init():
    all_tables = tables.get_tables()
    for tableArray in all_tables:
        for table in tableArray:
            if table_exists(table, connection):
                print("Table {} exists.".format(table))
            else:
                print("Table {} does not exist.".format(table))
                print("Creating table {}.".format(table))



healthButton = st.button("Health")
goalsButton = st.button("Goals")
userButton = st.button("User")

def initialize_webclient():
    pass

