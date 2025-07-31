# pages/bmi_analyzer.py
import streamlit as st
import os
from dotenv import load_dotenv
import database
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="BMI Analysis", page_icon="🔬")

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🔴 Google API Key not found.")
    st.stop()

if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("You must be logged in. Please return to the main page.")
    st.stop()

user_id = st.session_state['user_id']
user_data = database.load_user_data(user_id)

if not user_data:
    st.error("Could not load user data. Please start over.")
    st.stop()

st.title("🔬 Step 2: Health Metrics Analysis")

try:
    weight = float(user_data['profile']['weight_kg'])
    height_m = float(user_data['profile']['height_cm']) / 100
    if height_m == 0: raise ValueError("Height cannot be zero.")
    bmi = round(weight / (height_m ** 2), 1)
    if bmi < 18.5: category = "Underweight"
    elif 18.5 <= bmi < 25: category = "Normal weight"
    elif 25 <= bmi < 30: category = "Overweight"
    else: category = "Obesity"
    st.metric(label="Your Calculated BMI", value=bmi)
    st.info(f"Category: **{category}**")
except (ValueError, TypeError, KeyError):
    st.error("Could not calculate BMI. Please ensure weight and height are entered correctly.")
    st.stop()

def get_bmi_interpretation(bmi_value, bmi_category, fitness_goal, api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.6)
    prompt = PromptTemplate.from_template(
        """You are an AI fitness assistant. Provide a brief, encouraging, non-medical interpretation of a user's BMI.
        **CRITICAL: DO NOT PROVIDE MEDICAL ADVICE.** Always include a disclaimer to consult a healthcare professional.
        User's BMI: {bmi_value} ({bmi_category})
        User's Fitness Goal: {fitness_goal}"""
    )
    chain = prompt | llm
    return chain.invoke({
        "bmi_value": bmi_value, "bmi_category": bmi_category, "fitness_goal": user_data['profile']['fitness_goal']
    }).content

with st.expander("🤖 See the AI's Interpretation"):
    with st.spinner("Analyzing..."):
        interpretation = get_bmi_interpretation(bmi, category, user_data['profile']['fitness_goal'], GOOGLE_API_KEY)
        st.markdown(interpretation)
        user_data["health_metrics"] = {"bmi_value": bmi, "bmi_category": category, "bmi_interpretation": interpretation}
        database.save_user_data(user_id, user_data)

st.write("---")
st.header("Ready to Build Your Plan?")
if st.button("💪 Generate My Full Plan!"):
    from agents.trainer_agent import create_workout_plan
    from agents.nutritionist_agent import create_nutrition_plan
    with st.spinner("Agent 2 (Master Trainer) is creating your workout plan..."):
        user_data["workout_plan"] = create_workout_plan(user_data["profile"], api_key=GOOGLE_API_KEY)
        database.save_user_data(user_id, user_data)
        st.success("Workout plan generated!")
    with st.spinner("Agent 3 (Dietitian) is crafting your nutrition plan..."):
        user_data["nutrition_plan"] = create_nutrition_plan(user_data["profile"], user_data["workout_plan"], api_key=GOOGLE_API_KEY)
        database.save_user_data(user_id, user_data)
        st.success("Nutrition plan generated!")
    st.success("Your complete plan is ready! Redirecting to your dashboard...")
    st.switch_page("pages/my_dashboard.py")