# pages/3_🤖_My_Dashboard.py
import streamlit as st
import json
import os
from dotenv import load_dotenv

# --- Library Imports ---
import database
from agents.coach_agent import get_motivational_advice
from agents.analysis_agent import analyze_and_update_plan

# --- LangChain Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

# --- Page Configuration and Setup ---
st.set_page_config(page_title="My Dashboard", page_icon="🤖", layout="wide")

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GOOGLE_API_KEY or not TAVILY_API_KEY:
    st.error("🔴 Google or Tavily API Key not found. Please ensure both are set in your .env file.")
    st.stop()

# --- Guard Clauses ---
if 'user_id' not in st.session_state or not st.session_state['user_id']: st.stop()
user_id = st.session_state['user_id']
user_data = database.load_user_data(user_id)
if not user_data or not user_data.get("nutrition_plan", user_data.get("original_nutrition_plan")): st.stop()


# --- Agent 5: The Orchestrator Setup Function (UPDATED WITH THE FIX) ---
def setup_chat_orchestrator(user_data, api_key):
    """Initializes the conversational agent with an improved, more robust prompt."""
    
    tools = [
        get_motivational_advice,
        TavilySearchResults(max_results=3, description="A search engine for up-to-date information on external topics like fitness trends, supplements, or research.")
    ]
    
    # --- THE DEFINITIVE FIX: A much stricter and clearer prompt with an example ---
    prompt_template = PromptTemplate.from_template(
        """You are the AI Fitness Architect, a master orchestrator. Your personality is encouraging and professional.
        Your primary purpose is to act as a conversational assistant. You must follow a strict reasoning process.

        **YOUR REASONING PROCESS:**
        The `Thought:` is your private, step-by-step reasoning. It is your internal monologue. **DO NOT** write your final answer or greet the user in your thought process.

        **SCENARIO 1: Simple Questions & Greetings**
        If the user asks a simple question that can be answered from their data OR if they just say "hi" or a similar greeting, you MUST reason about it in your `Thought:` and then immediately provide a `Final Answer:`. You should not use the Action/Action Input sequence for this.

        **EXAMPLE FOR SCENARIO 1:**
        Question: Hi there!
        Thought: The user is giving a simple greeting. I will respond in a friendly and professional manner and ask how I can help. I do not need a tool for this. I will proceed directly to the Final Answer.
        Final Answer: Hello! I'm your AI Fitness Architect, ready to help. What can I do for you today?

        **SCENARIO 2: Questions Requiring Tools**
        If and only if the question requires external knowledge (`tavily_search_results_json`) or emotional support (`get_motivational_advice`), you MUST use the full `Action/Action Input/Observation` sequence.

        **HERE IS THE USER's COMPLETE DATA:**
        {user_data_json}

        **AVAILABLE TOOLS:**
        {tools}

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
        """
    )
    
    prompt = prompt_template.partial(
        user_data_json=json.dumps(user_data, indent=2),
        tools="\n".join([f"{repr(tool)}" for tool in tools]),
        tool_names=", ".join([tool.name for tool in tools])
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.6)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)

# --- Main App UI (No changes needed below this line) ---
st.title(f"🤖 Welcome to your Dashboard, {user_id}!")

st.write("---")
st.subheader("🚀 Adaptive Planning (Advanced Feature)")
st.markdown("Feeling stuck? Let our Analysis Agent review your progress and suggest an updated plan.")
if st.button("Analyze My Progress & Update My Plan"):
    with st.spinner("Analysis Agent is reviewing your logs and consulting with other agents..."):
        update_result = analyze_and_update_plan(user_data, GOOGLE_API_KEY)
        if update_result["status"] == "Plan Updated":
            if not user_data.get("original_workout_plan"):
                user_data["original_workout_plan"] = user_data.get("workout_plan")
                user_data["original_nutrition_plan"] = user_data.get("nutrition_plan")
            user_data["updated_workout_plan"] = update_result["updated_workout_plan"]
            user_data["updated_nutrition_plan"] = update_result["updated_nutrition_plan"]
            database.save_user_data(user_id, user_data)
            st.success("Your plan has been updated successfully!")
            st.balloons()
            st.rerun()
        else:
            st.info("Analysis complete: No plan update is needed right now.")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

orchestrator = setup_chat_orchestrator(user_data, api_key=GOOGLE_API_KEY)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "💪 Workout", "🥗 Nutrition", "🔬 Health Metrics", "👤 Profile"])

with tab1:
    st.subheader("Chat with your AI Architect (Agent 5)")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = orchestrator.invoke({
                    "input": prompt, "fitness_goal": user_data["profile"]["fitness_goal"]
                })
                full_response = response['output']
                st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tab2:
    st.subheader("Your Workout Plan")
    if user_data.get("updated_workout_plan"):
        st.info("Displaying your **latest updated** workout plan.")
        st.markdown(user_data["updated_workout_plan"])
        with st.expander("View Original Plan"):
            st.markdown(user_data.get("original_workout_plan", "Not available."))
    else:
        st.markdown(user_data.get("workout_plan", "Not generated yet."))

with tab3:
    st.subheader("Your Nutrition Plan")
    if user_data.get("updated_nutrition_plan"):
        st.info("Displaying your **latest updated** nutrition plan.")
        st.markdown(user_data["updated_nutrition_plan"])
        with st.expander("View Original Plan"):
            st.markdown(user_data.get("original_nutrition_plan", "Not available."))
    else:
        st.markdown(user_data.get("nutrition_plan", "Not generated yet."))

with tab4:
    st.subheader("Your Baseline Health Metrics")
    health_metrics = user_data.get("health_metrics", {})
    st.metric("Body Mass Index (BMI)", health_metrics.get("bmi_value", "N/A"))
    st.info(f"Category: **{health_metrics.get('bmi_category', 'N/A')}**")
    with st.expander("View AI Interpretation"):
        st.markdown(health_metrics.get("bmi_interpretation", "No interpretation."))

with tab5:
    st.subheader("Your Profile Data")
    st.json(user_data.get("profile", {}))

st.sidebar.title("Navigation")
if st.sidebar.button("Logout"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.switch_page("app.py")