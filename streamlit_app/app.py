import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

st.title("Team CRUD App")

# CREATE
with st.form("create"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit = st.form_submit_button("Add")

    if submit:
        with engine.connect() as conn:
            conn.execute(
                f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
            )
        st.success("Added!")

# READ
df = pd.read_sql("SELECT * FROM users", engine)
st.write(df)