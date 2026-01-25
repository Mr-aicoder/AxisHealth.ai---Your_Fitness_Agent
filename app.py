# app.py   
import streamlit as st     
import database      

st.set_page_config(
    page_title="Welcome to AxisHealth.ai",
    page_icon="👋",
)        
  
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

st.sidebar.title("User Management")

if not st.session_state.user_id:
    with st.sidebar.form(key='login_form'):
        user_id_input = st.text_input("Enter User ID to Login or Register")   
        login_button = st.form_submit_button("Login / Register") 
        if login_button and user_id_input:
            st.session_state['user_id'] = user_id_input
            st.rerun()
        elif login_button:
            st.sidebar.error("Please enter a User ID.")
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.user_id}**")
    if st.sidebar.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun() 

st.title("Welcome to 🤖 AxisHealth.ai")
st.caption("Your Fitness Agent") 

if not st.session_state.user_id:
    st.header("Login to Get Started")
    st.markdown("Please use the sidebar to log in or register with a new User ID.")  
else:
    user_data = database.load_user_data(st.session_state.user_id)
    if user_data and user_data.get("nutrition_plan"):
        st.switch_page("pages/my_dashboard.py") 
    else:

        st.switch_page("pages/get_started.py")    
      
  

