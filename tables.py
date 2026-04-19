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

if not connection.is_connected():
    print("Error connecting to MySQL database.")
    print("Please check your credentials and you are connected to the NTNU vpn and try again.")
    quit(0)


def create_table(name):
    pass


def read_table(name):
    query = f"SELECT * FROM {name}"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    return pd.DataFrame(rows, columns=columns)



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
    for table_Array in tables:
     if table_exists(table_Array):
            print("Table {} exists.".format(table_Array))
     else:
            print("Table {} does not exist.".format(table_Array))


def get_dataframe_from_table(name_of_table):
    return pd.read_sql(f"SELECT * FROM {name_of_table}", connection)

def update_user(user_id, name, email, password, gender, date_of_birth, height):
        cursor = connection.cursor()
        query = """
            UPDATE users
            SET name = %s,
                email = %s,
                password = %s,
                gender = %s,
                date_of_birth = %s,
                height = %s
            WHERE user_id = %s
        """
        cursor.execute(
            query,
            (name, email, password, gender, date_of_birth, height, user_id)
        )
        connection.commit()
        cursor.close()


def get_user_by_id(user_id):
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

