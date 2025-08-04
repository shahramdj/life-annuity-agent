def compliance_check(profile: dict, product: str) -> str:
    """
    Check if the recommended product complies with the customer's risk profile.
    Returns a compliance message.
    """
    if profile["risk_tolerance"] == "low" and "Variable" in product:
        return "⚠️ May not match risk profile."
    return "✅ Suitable recommendation."
