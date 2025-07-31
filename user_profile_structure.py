# user_profile_structure.py

def get_initial_profile_data(user_id):
    """Returns the dictionary structure for a new user."""
    return {
        "user_id": user_id,
        "profile": {
            'gender': None, 'age': None, 'weight_kg': None, 'height_cm': None,
            'fitness_goal': None, 'experience_level': None, 'available_equipment': None,
            'time_per_week': None, 'dietary_preference': None, 'allergies': None,
        },
        "health_metrics": {
            "bmi_value": None,
            "bmi_category": None,
            "bmi_interpretation": None,
        },
        "workout_log": [], 
        "original_workout_plan": None,
        "original_nutrition_plan": None,
        "updated_workout_plan": None,
        "updated_nutrition_plan": None,
    }