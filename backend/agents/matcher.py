from cursor import agent, tool

@tool
def fetch_annuity_products(risk: str, type: str) -> list:
    return [
        {"name": "Lifetime Secure Annuity", "type": "fixed", "risk": "low", "provider": "Acme Insurance"},
        {"name": "Indexed Growth Annuity", "type": "indexed", "risk": "moderate", "provider": "TrustLife"},
        {"name": "Market Plus Variable", "type": "variable", "risk": "high", "provider": "FinSecure"},
    ]

@agent
def match_annuity_product(profile: dict) -> dict:
    if profile["retired"] and profile["risk_tolerance"] == "low":
        return {"recommended_product": "Immediate Fixed Annuity"}
    return {"recommended_product": "Deferred Variable Annuity"}
