# pages/5_🍽️_Meal_Calculator.py
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Meal Calculator", page_icon="🍽️")

# --- API Key Loading and Validation ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🔴 Google API Key not found. Please ensure it is set in your .env file.")
    st.stop()

# --- The "Meal Calculator Agent" Function ---
def get_meal_analysis(meal_description: str, api_key: str):
    """Uses an LLM to analyze a meal description and estimate nutritional info."""
    print("--- Running Meal Calculator Agent ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.2)
    
    prompt = PromptTemplate.from_template(
        """You are an expert food analyst. Your task is to calculate the estimated nutritional information for the following meal description provided by a user.

        **Instructions:**
        1.  Analyze the user's input: `{meal_description}`.
        2.  Break the meal down into its core ingredients.
        3.  For each ingredient, estimate a reasonable quantity if not specified.
        4.  Calculate the approximate calories, protein (g), carbohydrates (g), and fat (g) for each ingredient.
        5.  Sum the totals for the entire meal.
        6.  Present the result in a clean, easy-to-read Markdown table.
        7.  Include a brief, one-sentence summary of the meal's nutritional profile (e.g., "This is a high-protein meal, great for post-workout recovery.").
        8.  Add a disclaimer at the bottom: "*Nutritional information is an estimate and can vary based on specific ingredients and preparation methods.*"

        Begin!
        """
    )
    
    chain = prompt | llm
    return chain.invoke({"meal_description": meal_description}).content


# --- Streamlit UI ---
st.title("🍽️ Meal Calorie Calculator Agent")
st.markdown("Enter the components of your meal below, and the AI will estimate its nutritional content.")

with st.form("meal_calculator_form"):
    meal_input = st.text_area("Describe your meal", "e.g., 150g grilled chicken breast, 200g cooked white rice, and a cup of steamed broccoli with a splash of olive oil", height=150)
    submit_button = st.form_submit_button("Analyze Meal")

if submit_button and meal_input:
    with st.spinner("AI is analyzing your meal..."):
        analysis_result = get_meal_analysis(meal_input, GOOGLE_API_KEY)
        st.markdown(analysis_result)

st.info("This is a standalone tool. The results are not currently saved to your user profile.", icon="ℹ️")
