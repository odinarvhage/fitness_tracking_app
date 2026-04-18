import os

import pandas as pd

import constants

import mysql.connector
from dotenv import load_dotenv

tables = constants.tables
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


def create_table(name):
    pass
#read_table assumes the table exists.
def read_table(name):
    query = f"SELECT * FROM {name}"
    return pd.read_sql(query, connection)



def table_exists(table_name):
    query = """
       SELECT COUNT(*)
       FROM information_schema.tables
       WHERE table_schema = %s
         AND table_name = %s
       """
    cursor = connection.cursor()
    cursor.execute(query, (connection.database, table_name))
    exists = cursor.fetchone()[0] == 1
    cursor.close()
    return exists

def status_check():
    for tableArray in tables:
     for table in tableArray:
            if table_exists(table):
                print("Table {} exists.".format(table))
            else:
                print("Table {} does not exist.".format(table))


def get_dataframe_from_table(name_of_table):
    return pd.read_sql(f"SELECT * FROM {name_of_table}", connection)
