# pages/4_📈_Log_Workout.py
import streamlit as st
import database
from datetime import datetime

st.set_page_config(page_title="Log Workout", page_icon="📈")

if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("You must be logged in to access this page.")
    st.stop()

user_id = st.session_state['user_id']
user_data = database.load_user_data(user_id)

st.title("📈 Log Your Workout")
st.markdown("Consistent tracking is the key to progress. Let's log your performance!")

with st.form("log_workout_form"):
    # In a real app, this would be a dropdown of exercises from their plan
    exercise_name = st.text_input("Exercise Name", "e.g., Barbell Squat")
    
    col1, col2 = st.columns(2)
    weight_lifted = col1.number_input("Weight (kg)", min_value=0.0, step=0.5)
    reps_completed = col2.number_input("Reps Completed", min_value=0, step=1)
    
    notes = st.text_area("How did it feel?", "e.g., Felt strong, last rep was tough.")
    
    submit_button = st.form_submit_button("Log This Set")

if submit_button:
    log_entry = {
        "date": datetime.now().isoformat(),
        "exercise": exercise_name,
        "weight_kg": weight_lifted,
        "reps": reps_completed,
        "notes": notes,
    }
    
    if "workout_log" not in user_data:
        user_data["workout_log"] = []
        
    user_data["workout_log"].append(log_entry)
    database.save_user_data(user_id, user_data)
    
    st.success(f"Successfully logged: {exercise_name} at {weight_lifted}kg for {reps_completed} reps!")
    st.balloons()

st.write("---")
st.subheader("Your Workout History")
if user_data.get("workout_log"):
    st.dataframe(user_data["workout_log"][::-1]) # Show latest first
else:
    st.info("No workouts logged yet.")