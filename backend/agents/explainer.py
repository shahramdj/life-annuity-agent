def explain_product(product_name: str) -> str:
    """
    Explain the features and benefits of a specific annuity product.
    Returns a description of the product.
    """
    descriptions = {
        "Immediate Fixed Annuity": "Provides guaranteed monthly income starting immediately.",
        "Deferred Variable Annuity": "Offers growth potential with market risk, suitable for long‑term goals."
    }
    return descriptions.get(product_name, "Product details not available.")
