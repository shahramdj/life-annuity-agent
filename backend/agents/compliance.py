from cursor import agent

@agent
def compliance_check(profile: dict, product: str) -> str:
    if profile["risk_tolerance"] == "low" and "Variable" in product:
        return "⚠️ May not match risk profile."
    return "✅ Suitable recommendation."
