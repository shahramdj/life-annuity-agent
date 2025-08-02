from cursor import agent

@agent
def profile_customer(conversation: str) -> dict:
    return {
        "age": "67",
        "retired": True,
        "risk_tolerance": "low",
        "income_goal": "guaranteed income for life"
    }
