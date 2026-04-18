import os

import streamlit as st
import mysql.connector
from dotenv import load_dotenv

import tables

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
    print("Please check your credentials and you are connected to the NTNU vpn and try again.")
    quit(0)


all_tables = tables.get_tables()
for tableArray in all_tables:
    for table in tableArray:
        if table_exists(table, connection):
            print("Table {} exists.".format(table))
        else:
            print("Table {} does not exist.".format(table))


healthButton = st.button("Health")
goalsButton = st.button("Goals")
userButton = st.button("User")

def initialize_webclient():
    pass
