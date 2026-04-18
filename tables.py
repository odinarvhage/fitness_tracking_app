
import pandas as pd
userTables = "users","workout","workout_entries","exercises","health_metric"
goalTables = "goals","weight_goals","sleep_goals","running_goals","strength_goals"
allTables = userTables,goalTables

def get_tables():
    return allTables

def create_table(name, conn):
    pass
#read_table assumes the table exists.
def read_table(name, conn):
    query = f"SELECT * FROM {name}"
    return pd.read_sql(query, conn)
