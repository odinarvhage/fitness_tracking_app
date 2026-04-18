
import pandas as pd
userTables = "User","Workout","WorkoutEntry","Exercise","HealthMetric"
goalTables = "Goal","WeightGoal","SleepGoal","RunningGoal","StrengthGoal"
allTables = userTables,goalTables

def get_tables():
    return allTables

def create_table(name, conn):
    pass
#read_table assumes the table exists.
def read_table(name, conn):
    query = f"SELECT * FROM {name}"
    return pd.read_sql(query, conn)
