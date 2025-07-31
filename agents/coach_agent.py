# agents/coach_agent.py
from langchain.agents import tool

@tool
def get_motivational_advice(user_feeling: str, fitness_goal: str) -> str:
    """Agent 4: Provides motivational support. Use this tool ONLY when a user expresses feelings of doubt, frustration, or lack of motivation."""
    print("\n>>> [Agent Log] Calling Agent 4: The Motivational Coach Tool...")
    return (
        f"I hear that you're feeling {user_feeling}. That's a very normal part of any "
        f"journey, especially one as important as your goal to {fitness_goal}. "
        "Remember that consistency is more important than perfection. You've got this."
    )