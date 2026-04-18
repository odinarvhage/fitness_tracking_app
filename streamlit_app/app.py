import os
import streamlit as st
import pandas as pd
import hashlib
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

st.title("Team CRUD App")

with st.form("create_user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    gender = st.selectbox(
        "Gender",
        ["", "Male", "Female", "Non-binary", "Prefer not to say"]
    )
    date_of_birth = st.date_input("Date of birth", value=None)
    height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, step=0.1)

    submitted = st.form_submit_button("Create user")


if submitted:
    errors = []

    if not name.strip():
        errors.append("Name is required.")
    if not email.strip():
        errors.append("Email is required.")
    if not password:
        errors.append("Password is required.")
    if not gender:
        errors.append("Gender is required.")
    if height <= 0:
        errors.append("Height must be greater than 0.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        try:
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO users
                        (name, email, password, gender, date_of_birth, height)
                        VALUES
                        (:name, :email, :password, :gender, :date_of_birth, :height)
                    """),
                    {
                        "name": name.strip(),
                        "email": email.strip(),
                        "password": password_hash,
                        "gender": gender,
                        "date_of_birth": date_of_birth,
                        "height": height,
                    },
                )

            st.success("User created successfully.")

        except Exception as e:
            st.error("Could not create user.")
            st.code(str(e))

st.subheader("Existing users")

try:
    df = pd.read_sql(
        """
        SELECT user_id, name, email, gender, date_of_birth, height
        FROM users
        ORDER BY user_id DESC
        """,
        engine,
    )
    st.dataframe(df, width='stretch')
except Exception as e:
    st.warning("Could not load users table.")
    st.code(str(e))