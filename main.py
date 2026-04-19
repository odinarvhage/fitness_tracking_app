import sys
from operator import truediv
import streamlit as st
import constants
import tables


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
    st.dataframe(tables.read_table("health_metric"), width='stretch')

#-------------------------
# GOALS RELATED DISPLAY
#-------------------------
elif page == "Goals":
    st.header("Goals")
    st.dataframe(tables.read_table("goals"), width='stretch')


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.dataframe(tables.read_table("weight_goals"), width='stretch')
    with col2:
        st.dataframe(tables.read_table("running_goals"), width='stretch')
    with col3:
        st.dataframe(tables.read_table("sleep_goals"), width='stretch')
    with col4:
        st.dataframe(tables.read_table("strength_goals"), width='stretch')
    with col5:
        st.dataframe(tables.read_table("steps_goals"), width='stretch')

#-------------------------
# USER RELATED DISPLAY
#-------------------------
elif page == "User":
    st.header("Users")

    try:
        df = tables.read_table("users")
        st.dataframe(df, width='stretch')
    except Exception as e:
        st.error(f"Could not load users: {e}")
        st.stop()

    

#-------------------------
# WORKOUT RELATED DISPLAY
#-------------------------
elif page == "Workout":
    st.header("workout")
    st.dataframe(tables.read_table("workout"), width='stretch')

    sub_workout = col1, col2 = st.columns(2)

    with col1:
        st.dataframe(tables.read_table("workout_entries"), width='stretch')
    with col2:
        st.dataframe(tables.read_table("exercises"), width='stretch')


#-------------------------
# DISPLAYS A POP UP DIALOG FOR CREATE
#-------------------------
@st.dialog("CREATE entry")
def create_entry():
    table_name = st.selectbox("Choose a table", list(constants.CREATE_TABLE.keys()))

    inputs = {}
    for col in constants.CREATE_TABLE[table_name]:
        inputs[col] = st.text_input(col)

    if st.button("Submit"):
        st.write("You entered:")
        st.json(inputs)
        st.rerun()


#-------------------------
# DISPLAYS A POP UP DIALOG FOR UPDATE
#-------------------------
@st.dialog("UPDATE entry")
def update_entry():
    table_name = st.selectbox("Choose a table", list(constants.UPDATE_TABLE.keys()))
    
    primary_key = constants.PRIMARY_KEYS[table_name]
    df = tables.read_table(table_name)

    if df.empty:
        st.info(f"No rows in {table_name}")
        return
    
    if primary_key not in df.columns:
        st.error(f"Primary key '{primary_key}' not found in dataframe columns: {df.columns.tolist()}")
        return

    row_ids = df[primary_key].tolist()
    selected_id = st.selectbox(f"Choose {primary_key}", row_ids, key="update_row_id")

    selected_row = tables.get_row_by_id(table_name, primary_key, selected_id)
    if not selected_row:
        st.error("Could not find selected row.")
        return
    
    updated_values = {}

    with st.form("update_form"):
        for col in constants.UPDATE_TABLE[table_name]:
            if col == primary_key:
                continue
            updated_values[col] = st.text_input(col, value=str(selected_row[col]) if selected_row[col] is not None else "") 
        
        submitted = st.form_submit_button("Update")
    
    if submitted:
        try:
            tables.update_row(table_name, primary_key, selected_id, updated_values)
            st.success(f"Updated entry in {table_name}")
            st.rerun()
        except Exception as e:
            st.error(f"Could not update entry: {e}")


#-------------------------
# CREATE ENTRY
#-------------------------
if create_button:
    create_entry()

#-------------------------
# DELETE ENTRY
#-------------------------
if delete_button:
    print("Deleting")

# -------------------------
# UPDATE ENTRY / FIELD
# -------------------------
if update_button:
    update_entry()
if sys.argv.__len__() > 1:
    if sys.argv[1] == "status":
        tables.status_check()


