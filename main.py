import sys
import streamlit as st
import tables

st.set_page_config(
    page_title="Fitness Tracking App",
    layout="wide"
)

st.title("Fitness Tracking App Demo - Group 5")

if "page" not in st.session_state:
    st.session_state.page = "User"


col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Health"):
        st.session_state.page = "Health"

with col2:
    if st.button("Goals"):
        st.session_state.page = "Goals"

with col3:
    if st.button("User"):
        st.session_state.page = "User"

with col4:
    if st.button("Workout"):
        st.session_state.page = "Workout"

page = st.session_state.page

if page == "Health":
    st.header("Health")
    st.dataframe(tables.read_table("health_metric"), use_container_width=true)

elif page == "Goals":
    st.header("Goals")
    st.dataframe(tables.read_table("goals"), use_container_width=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.dataframe(tables.read_table("weight_goals"), use_container_width=True)
    with col2:
        st.dataframe(tables.read_table("running_goals"), use_container_width=True)
    with col3:
        st.dataframe(tables.read_table("sleep_goals"), use_container_width=True)
    with col4:
        st.dataframe(tables.read_table("strength_goals"), use_container_width=True)
    with col5:
        st.dataframe(tables.read_table("steps_goals"), use_container_width=True)

elif page == "User":
    st.header("Users")

    try:
        df = tables.read_table("users")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load users: {e}")
        st.stop()

    st.subheader("Update existing user")

    if df.empty:
        st.info("No users found.")
    else:
        user_ids = df["user_id"].tolist()
        selected_user_id = st.selectbox("Select user ID to edit", user_ids)

        selected_user = tables.get_user_by_id(selected_user_id)

        if selected_user:
            gender_options = ["Male", "Female", "Other"]
            current_gender = selected_user["gender"] if selected_user["gender"] in gender_options else "Other"

            with st.form("update_user_form"):
                updated_name = st.text_input("Name", value=selected_user["name"] or "")
                updated_email = st.text_input("Email", value=selected_user["email"] or "")
                updated_password = st.text_input("Password", value=selected_user["password"] or "", type="password")
                updated_gender = st.selectbox(
                    "Gender",
                    gender_options,
                    index=gender_options.index(current_gender)
                )
                updated_date_of_birth = st.date_input("Date of birth", value=selected_user["date_of_birth"])
                updated_height = st.number_input(
                    "Height (cm)",
                    min_value=0.0,
                    max_value=300.0,
                    step=0.1,
                    value=float(selected_user["height"]) if selected_user["height"] is not None else 0.0
                )

                update_submitted = st.form_submit_button("Update user")

            if update_submitted:
                try:
                    tables.update_user(
                        selected_user_id,
                        updated_name,
                        updated_email,
                        updated_password,
                        updated_gender,
                        updated_date_of_birth,
                        updated_height
                    )
                    st.success("User updated successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not update user: {e}")

elif page == "Workout":
    st.header("workout")
    st.dataframe(tables.read_table("workout"), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(tables.read_table("workout_entries"), use_container_width=True)
    with col2:
        st.dataframe(tables.read_table("exercises"), use_container_width=True)



if sys.argv.__len__() > 1:
    if sys.argv[1] == "status":
        tables.status_check()



