import streamlit as st
import internal


st.set_page_config(
    page_title="Fitness Tracking App",
    layout="wide"
)

st.title("Fitness Tracking App Demo - Group 5")


if "page" not in st.session_state:
    st.session_state.page = "User"


buttons = col1, col2, col3, col4, col5, col6, col7= st.columns(7)



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
with col5:
    create_button = st.button("CREATE")
with col6:
    delete_button = st.button("DELETE")
with col7:
    update_button = st.button("UPDATE")

page = st.session_state.page

#-------------------------
# HEALTH RELATED DISPLAY
#-------------------------
if page == "Health":
    st.header("Health")
    st.dataframe(internal.read_table("health_metric"), width='stretch')

#-------------------------
# GOALS RELATED DISPLAY
#-------------------------
elif page == "Goals":
    st.header("Goals")
    st.dataframe(internal.read_table("goals"), width='stretch')


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.dataframe(internal.read_table("weight_goals"), width='stretch')
    with col2:
        st.dataframe(internal.read_table("running_goals"), width='stretch')
    with col3:
        st.dataframe(internal.read_table("sleep_goals"), width='stretch')
    with col4:
        st.dataframe(internal.read_table("strength_goals"), width='stretch')
    with col5:
        st.dataframe(internal.read_table("steps_goals"), width='stretch')

#-------------------------
# USER RELATED DISPLAY
#-------------------------
elif page == "User":
    st.header("Users")

    try:
        df = internal.read_table("users")
        st.dataframe(df, width='stretch')
    except Exception as e:
        st.error(f"Could not load users: {e}")
        st.stop()

    

#-------------------------
# WORKOUT RELATED DISPLAY
#-------------------------
elif page == "Workout":
    st.header("workout")
    st.dataframe(internal.read_table("workout"), width='stretch')

    sub_workout = col1, col2 = st.columns(2)

    with col1:
        st.dataframe(internal.read_table("workout_entries"), width='stretch')
    with col2:
        st.dataframe(internal.read_table("exercises"), width='stretch')




#-------------------------
# CREATE ENTRY
#-------------------------
if create_button:
    internal.create_entry()

#-------------------------
# DELETE ENTRY
#-------------------------
if delete_button:
    print("Deleting")

# -------------------------
# UPDATE ENTRY / FIELD
# -------------------------
if update_button:
    internal.update_entry()