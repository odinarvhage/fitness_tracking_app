create_tables = {
    "User": [
        "Name","Password", "Email", "Gender", "Height", "Date of birth"
    ],
    "Workout": [
        "Duration", "Type", "Calories burned", "Date"
    ],
    "Health metric": [
        "Weight", "Resting heart rate", "Average sleep", "Steps", "Date"
    ]
}

db_tables = {
    "users": [
        "user_id", "name","email","password", "gender", "date_of_birth", "height"
    ],
    "workout": [
        "workout_id", "user_id", "duration", "type", "calories_burned", "workout_date"
    ],
    "health_metric": [
        "metric_id", "user_id", "weight", "resting_heart_rate", "average_sleep", "steps", "recorded_date"
    ]
}

update_tables = {
    "users": [
        "user_id", "name", "email", "password", "gender", "date_of_birth", "height"
    ],
    "workout": [
        "workout_id", "user_id", "duration", "type", "calories_burned", "workout_date"
    ],
    "health_metric": [
        "metric_id", "user_id", "weight", "resting_heart_rate", "average_sleep", "steps", "recorded_date"
    ]
}


