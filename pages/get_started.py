# pages/get_started.py
import streamlit as st
import database
from user_profile_structure import get_initial_profile_data

st.set_page_config(page_title="Onboarding", page_icon="🚀")

if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("You must be logged in. Please return to the main page to log in.")
    st.stop()

user_id = st.session_state['user_id']

st.title("🚀 Step 1: Tell Us About Yourself")
st.info(f"Creating profile for User ID: **{user_id}**")

with st.form(key='onboarding_form'):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    age = col1.number_input("Age", 13, 100, 25)
    weight_kg = col1.number_input("Weight (kg)", 30.0, 250.0, 70.0, 0.5, "%.1f")
    gender = col2.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
    height_cm = col2.number_input("Height (cm)", 100.0, 250.0, 175.0, 0.5, "%.1f")
    st.subheader("Fitness Goals & Experience")
    fitness_goal = st.text_input("Primary fitness goal?", "e.g., lose 10kg, gain muscle")
    experience_level = st.selectbox("Fitness experience level?", ["Beginner", "Intermediate", "Advanced"])
    time_per_week = st.selectbox("How many days per week can you train?", ["1-2", "3-4", "5+"])
    st.subheader("Preferences & Restrictions")
    available_equipment = st.selectbox("Equipment access?", ["No equipment", "Dumbbells/bands", "Full gym access"])
    dietary_preference = st.selectbox("Dietary preferences?", ["Anything", "Non Vegetarian", "Vegetarian", "Vegan", "Low-carb"])
    allergies = st.text_input("Any food allergies?", "none")
    submit_button = st.form_submit_button(label='Next Step: BMI Analysis →')

if submit_button:
    user_data = get_initial_profile_data(user_id)
    profile = user_data["profile"]
    profile.update({
        'gender': gender, 'age': age, 'weight_kg': weight_kg, 'height_cm': height_cm,
        'fitness_goal': fitness_goal, 'experience_level': experience_level,
        'time_per_week': time_per_week, 'available_equipment': available_equipment,
        'dietary_preference': dietary_preference, 'allergies': allergies
    })
    database.save_user_data(user_id, user_data)
    st.success("Profile saved! Redirecting...")
    st.switch_page("pages/bmi_analyzer.py")