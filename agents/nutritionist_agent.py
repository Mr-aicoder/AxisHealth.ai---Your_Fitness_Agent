# agents/nutritionist_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def create_nutrition_plan(profile_data, workout_plan, api_key):
    """Agent 3's core logic. Uses profile AND workout plan to create a diet plan."""
    print("\n--- Running Agent 3: The Dietitian & Nutritionist ---")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key,
        temperature=0.5,
        convert_system_message_to_human=True
    )

    prompt = PromptTemplate.from_template(
        """You are an expert nutritionist. Based on the user's profile and workout plan, create a daily meal plan.
        USER PROFILE:
        - Goal: {fitness_goal}
        - Dietary Preference: {dietary_preference}
        - Allergies: {allergies}
        USER'S WORKOUT PLAN SUMMARY:
        {workout_plan}
        Calculate an estimated daily calorie target and provide meal ideas for breakfast, lunch, dinner, and one snack. Format with Markdown."""
    )
    chain = prompt | llm
    plan = chain.invoke({**profile_data, "workout_plan": workout_plan}).content
    print("...Nutrition plan generated.")
    return plan