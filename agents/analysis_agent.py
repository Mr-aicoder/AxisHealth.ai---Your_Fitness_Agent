# agents/analysis_agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agents.trainer_agent import create_workout_plan
from agents.nutritionist_agent import create_nutrition_plan

def analyze_and_update_plan(user_data, api_key):
    """
    Analyzes user's workout log, detects plateaus, and triggers other agents
    to generate an updated plan.
    """
    print("\n--- Running Analysis Agent ---")
    
    # In a real app, this logic would be much more complex (e.g., checking
    # strength increases over the last 3 weeks for key compound lifts).
    # For this prototype, we'll simulate the detection of a plateau.
    plateau_detected = True # Simulate finding a plateau
    analysis_notes = "User has shown no significant strength increase in key lifts like 'Barbell Squat' over the last two weeks. Applying progressive overload is recommended."

    if not plateau_detected:
        return {"status": "No change needed", "notes": "Progress is looking good! Keep up the great work."}

    print("...Plateau detected. Generating updated plans.")

    # --- Re-call the Trainer Agent with new instructions ---
    print("...Calling Trainer Agent for updated workout plan.")
    profile_with_new_goal = user_data["profile"].copy()
    profile_with_new_goal["fitness_goal"] = (
        f"The user's original goal was '{user_data['profile']['fitness_goal']}'. "
        f"However, they have hit a plateau. Your task is to UPDATE their previous workout plan. "
        f"Based on the analysis: '{analysis_notes}', introduce progressive overload principles. "
        f"Slightly increase weight/intensity and consider swapping one accessory exercise."
    )
    updated_workout = create_workout_plan(profile_with_new_goal, api_key)

    # --- Re-call the Nutritionist Agent with new instructions ---
    print("...Calling Nutritionist Agent for updated nutrition plan.")
    updated_nutrition = create_nutrition_plan(user_data["profile"], updated_workout, api_key)
    
    return {
        "status": "Plan Updated",
        "notes": analysis_notes,
        "updated_workout_plan": updated_workout,
        "updated_nutrition_plan": updated_nutrition
    }