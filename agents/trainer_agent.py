# agents/trainer_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def create_workout_plan(profile_data, api_key):
    """Agent 2's core logic. Generates a workout plan using Google's Gemini model."""
    print("\n--- Running Agent 2: The Master Trainer ---")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key, 
        temperature=0.5, 
        convert_system_message_to_human=True
    )

    prompt = PromptTemplate.from_template(
        """You are an expert personal trainer. Based on the following user profile, create a detailed, 
        effective, and safe weekly workout plan.
        USER PROFILE:
        - Goal: {fitness_goal}
        - Experience: {experience_level}
        - Time: {time_per_week} days/week
        - Equipment: {available_equipment}
        Create a plan with a clear weekly split. For each day, list 5-6 exercises with sets and reps. Format with Markdown."""
    )
    chain = prompt | llm
    plan = chain.invoke(profile_data).content
    print("...Workout plan generated.")
    return plan