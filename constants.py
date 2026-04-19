tables = {
    "User": [
        "Name","Password", "Gender", "Height"
    ],
    "Workout": [
        "Duration", "Type", "Calories burned", "Date"
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
    "weight_goal": [
        "goal_id", "target_weight"
    ],
    "running_goal": [
        "goal_id", "target_distance", "target_time"
    ],
    "sleep_goal": [
        "goal_id", "target_sleep_duration"
    ],
    "steps_goal": [
        "goal_id", "target_steps_per_day"
    ],
    "strength_goal": [
        "goal_id", "target_weight", "target_reps", "exercise_id"
    ]
}