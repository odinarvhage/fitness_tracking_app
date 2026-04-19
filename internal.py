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

if not connection.is_connected():
    print("Error connecting to MySQL database.")
    print("Please check your credentials and you are connected to the NTNU vpn and try again.")
    quit(0)


def read_table(name):
    query = f"SELECT * FROM {name}"
    cursor = connection.cursor()
    cursor.execute(query)
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
    auto_skip = {"user_id", "workout_id", "metric_id"}
    return [col for col in columns if col not in auto_skip]


def get_dataframe_from_table(name_of_table):
    return pd.read_sql(f"SELECT * FROM {name_of_table}", connection)


def insert_row(table_name, values_dict):
    columns = list(values_dict.keys())
    values = list(values_dict.values())

    placeholders = ", ".join(["%s"] * len(values))
    column_names = ", ".join(columns)

    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

def get_row_by_id(table_name, primary_key, row_id):
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {table_name} WHERE {primary_key} = %s"
    cursor.execute(query, (row_id,))
    row = cursor.fetchone()
    cursor.close()
    return row   

def update_row(table_name, primary_key, row_id, values_dict):
    set_clause = ", ".join([f"{col} = %s" for col in values_dict.keys()])
    values = list(values_dict.values())
    values.append(row_id)

    query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


@st.dialog("CREATE entry")
def make_entry_dialog():
    table_name = st.selectbox("Choose a table", list(constants.CREATE_TABLE.keys()))
    data = {}
    for col in constants.CREATE_TABLE[table_name]:
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


def delete_entry(table, primary_key):
    cursor = connection.cursor()
    row = constants.PRIMARY_KEYS[table]
    sql = f"DELETE FROM `{table}` WHERE `{row}` = %s"
    cursor.execute(sql, (primary_key,))
    connection.commit()
# -------------------------
# DISPLAYS A POP UP DIALOG FOR UPDATE
# -------------------------
@st.dialog("UPDATE entry")
def update_entry():
    table_name = st.selectbox("Choose a table", list(constants.UPDATE_TABLE.keys()))

    primary_key = constants.PRIMARY_KEYS[table_name]
    df = read_table(table_name)

    if df.empty:
        st.info(f"No rows in {table_name}")
        return

    if primary_key not in df.columns:
        st.error(f"Primary key '{primary_key}' not found in dataframe columns: {df.columns.tolist()}")
        return

    row_ids = df[primary_key].tolist()
    selected_id = st.selectbox(f"Choose {primary_key}", row_ids, key="update_row_id")

    selected_row = get_row_by_id(table_name, primary_key, selected_id)
    if not selected_row:
        st.error("Could not find selected row.")
        return

    updated_values = {}

    with st.form("update_form"):
        for col in constants.UPDATE_TABLE[table_name]:
            if col == primary_key:
                continue
            updated_values[col] = st.text_input(col,
                                                value=str(selected_row[col]) if selected_row[col] is not None else "")

        submitted = st.form_submit_button("Update")

    if submitted:
        try:
            update_row(table_name, primary_key, selected_id, updated_values)
            st.rerun()
        except Exception as e:
            st.error(f"Could not update entry: {e}")


@st.dialog("DELETE entry")
def make_delete_dialog():
    table_name = st.selectbox("Choose a table", list(constants.db_tables.keys()))

    primary_key = constants.PRIMARY_KEYS[table_name]
    table = read_table(table_name)

    if table.empty:
        st.info(f"No rows in {table_name}")
        return

    row_ids = table[primary_key].tolist()
    selected_id = st.selectbox(f"Choose {primary_key}", row_ids, key="update_row_id")

    selected_row = get_row_by_id(table_name, primary_key, selected_id)
    if not selected_row:
        st.error("Could not find selected row.")
        return

    st.json(selected_row)
    deleted = st.button("Delete")

    if deleted:
        try:
            delete_entry(table_name, selected_id)
            st.rerun()

        except Exception as e:
            st.error(f"Could not delete entry: {e}")
