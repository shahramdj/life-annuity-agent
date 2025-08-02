from cursor import agent

@agent
def explain_product(product_name: str) -> str:
    descriptions = {
        "Immediate Fixed Annuity": "Provides guaranteed monthly income starting immediately.",
        "Deferred Variable Annuity": "Offers growth potential with market risk, suitable for long‑term goals."
    }
    return descriptions.get(product_name, "Product details not available.")
