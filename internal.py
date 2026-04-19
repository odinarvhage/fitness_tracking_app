import datetime
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

    real_table = constants.db_tables[table]
    insert_columns = []
    insert_values = []

    for col in real_table:
        if "id" in col:
            continue
        if col in values:
            insert_columns.append(col)
            if "date" in col:
                insert_values.append(str(values[col]))
            else:
                insert_values.append(values[col])

    col_sql = ", ".join(f"`{c}`" for c in insert_columns)
    placeholders = ", ".join(["%s"] * len(insert_columns))
    query = f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})"
    cursor = connection.cursor()
    cursor.execute(query, insert_values)
    connection.commit()
    cursor.close()

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
    with st.form("create_entry"):
        values = {}
        for key in constants.CREATE_TABLE[table_name]:
            if "date" in key:
                values[key] = st.date_input(key,   min_value=datetime.date(1900, 1, 1))
            elif "gender" in key:
                values[key] = st.selectbox("gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
            else:
                values[key] = st.text_input(key)
        submit_button = st.form_submit_button("create")

    if submit_button:
        missing = []
        for key, val in values.items():
            if isinstance(val, str) and val.strip() == "":
                missing.append(key)
            if "date" in key and val is None:
                missing.append(key)
        if missing:
            st.error(f"These fields cannot be empty: {', '.join(missing)}")
            return
        try:
            create_entry(table_name, values)
            st.rerun()
        except Exception as e:
            st.error(f"Could not create entry. {e}")


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
