# AxisHealth.ai- Your Fitness Agent 🤖

Welcome to **AxisHealth.ai**, your intelligent fitness companion powered by advanced AI agents and adaptive planning. This project leverages Streamlit, LangChain, and Google Gemini to deliver a personalized dashboard for health, nutrition, and workout management.
 

https://github.com/user-attachments/assets/10cd2f3a-bdf7-4d22-8214-b44d0100ed8e







# 🚀 Features

## Phase 1: User Onboarding and Health Metrics Analysis 
This is the foundational phase where the system establishes a new user's profile and
provides an initial health baseline.

#### 1. Login and Profile Creation: 
The user starts by logging in or registering with a 
unique user_id on the main page (app.py). They are then directed to the 
get_started.py page where they provide personal information such as age, weight, 
and fitness goals. This data is used to create a structured profile based on the 
user_profile_structure.py schema and is saved to the user_db.json file. 
#### 2. Initial BMI Analysis: 
The user is then automatically directed to the 
bmi_analyzer.py page. The system calculates their BMI using the weight and 
height from their profile. It then uses an LLM to provide a brief, non-medical 
interpretation of their BMI and saves this to their profile, establishing a crucial 
health baseline.

## Phase 2: Core Plan Generation 
Once the user's profile and initial health metrics are established, this phase focuses on
generating their personalized workout and nutrition plans. 
#### 1. Workout Plan Generation: 
On the bmi_analyzer.py page, the user can trigger the 
generation of a workout plan. The trainer_agent.py acts as an "expert personal 
trainer" and uses an LLM to create a detailed weekly workout plan based on the 
user's fitness goals, experience level, and available equipment. 
#### 2. Nutrition Plan Generation: 
Following the workout plan, the nutritionist_agent.py 
acts as a "dietitian & nutritionist". It uses the user's profile and the new workout 
plan to create a daily meal plan, including an estimated calorie target and 
macronutrient breakdown. Both of these plans are then saved to the user's profile.

## Phase 3: Adaptive Planning and Ongoing Engagement 
This final phase focuses on making the project a dynamic and long-term health 
companion. 
#### 1. Workout Tracking: 
The user can log their workout details, such as exercise name, 
weight, and reps, on the log_workout.py page. This data is appended to their 
workout_log in the database, allowing for progress tracking. 
#### 2. Adaptive Planning: 
A key feature is the analysis_agent.py, which is an "advanced 
feature" triggered by a button on the dashboard (my_dashboard.py). This agent's 
logic can detect a plateau in the user's progress and will automatically re-invoke 
the trainer_agent and nutritionist_agent with new instructions to generate a more 
challenging, updated plan. 
#### 3. AI Chatbot: 
The user can interact with the conversational 
"AI Fitness Architect" on the dashboard. This agent can use tools like the 
coach_agent.py for motivational support or search the web for external 
knowledge to provide up-to-date information, making the platform a dynamic and 
engaging companion for the user's fitness journey. 
#### 4. Meal Calculator: 
This agent helps in calculating the macro nutrients like Protein, Carbs, Fats and the overall calories in the meal.
The meal calculator works by taking a user's text description of a meal and using a generative AI model to estimate the nutritional content. It analyzes the text, identifies ingredients, estimates quantities, and calculates the approximate calories, protein, carbohydrates, and fat, presenting the results in a formatted table.

<img width="1668" height="712" alt="Axishealth -- Diagram" src="https://github.com/user-attachments/assets/05279995-a1a2-4575-84ca-659860803f37" />
---

## 🛠️ Tech Stack

- **Streamlit** — Interactive web UI
- **LangChain** — Agent orchestration and prompt engineering
- **Google Gemini** — Conversational LLM
- **Tavily Search** — Real-time external information
- **Python** — Core logic and data handling

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mr-aicoder/AxisHealth.ai---Your_Fitness_Agent.git
   cd AxisHealth.ai---Your_Fitness_Agent
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   ```
   GOOGLE_API_KEY=your_google_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

---

## ▶️ Usage

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Log in and explore your dashboard:**
   - Chat with your AI Fitness Architect
   - Review and update your workout and nutrition plans
   - Track your health metrics and progress



## 🧠 How It Works

- **Agent Orchestration:**  
  The orchestrator agent uses your profile and goals to deliver tailored responses and recommendations.

- **Adaptive Planning:**  
  The Analysis Agent reviews your logs and updates your plans using the latest research and motivational strategies.

- **Session Management:**  
  All interactions and updates are tracked per user for a seamless experience.

---

## 💡 Contributing

Pull requests and suggestions are welcome!  
Please open an issue for bug reports or feature requests.

---

## 📜 License

This project is licensed under the MIT License.

---

## ✨ Credits

Developed by [Mr-aicoder](https://github.com/Mr-aicoder)  


---










