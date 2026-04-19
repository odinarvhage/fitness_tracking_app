
DB_TABLE_COLUMNS = {
    "users": [
        "user_id", "name", "email", "password", "gender", "date_of_birth", "height"
    ],
    "workout": [
        "workout_id", "user_id", "duration", "type", "calories_burned", "workout_date"
    ],
    "workout_entries": [
        "workout_entry_id", "workout_id", "exercise_id", "reps", "sets", "weight_used", "distance"
    ],
    "exercises": [
        "exercise_id", "name", "description"
    ],
    "health_metric": [
        "metric_id", "user_id", "weight", "resting_heart_rate", "average_sleep", "steps", "recorded_date"
    ],
    "goals": [
        "goal_id", "user_id", "start_date", "deadline", "status"
    ],
    "weight_goals": [
        "goal_id", "target_weight"
    ],
    "running_goals": [
        "goal_id", "target_distance", "target_time"
    ],
    "sleep_goals": [
        "goal_id", "target_sleep_duration"
    ],
    "steps_goals": [
        "goal_id", "target_steps_per_day"
    ],
    "strength_goals": [
        "goal_id", "target_weight", "target_reps", "exercise_id"
    ]
}

UPDATE_TABLE = {
    "users": [
         "name", "password", "gender", "height"
    ]
}

CREATE_TABLE = {
    "users": [
         "name", "email", "password", "gender", "date_of_birth", "height"
    ]
}

PRIMARY_KEYS = {
    "users": "user_id",
    "workout": "workout_id",
    "workout_entries": "workout_entry_id",
    "exercises": "exercise_id",
    "health_metric": "metric_id",
    "goals": "goal_id",
    "weight_goals": "goal_id",
    "running_goals": "goal_id",
    "sleep_goals": "goal_id",
    "steps_goals": "goal_id",
    "strength_goals": "goal_id"
}