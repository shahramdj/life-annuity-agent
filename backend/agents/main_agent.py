from agents.profiler import profile_customer
from agents.matcher import match_annuity_product, fetch_annuity_products
from agents.calculator import calculate_annuity_income
from agents.explainer import explain_product
from agents.compliance import compliance_check

def annuity_recommendation_agent(conversation: str) -> str:
    """
    Main annuity recommendation agent that orchestrates all sub-agents.
    Takes a conversation string and returns a comprehensive recommendation.
    """
    # Profile the customer based on their conversation
    profile = profile_customer(conversation)
    
    # Match an appropriate annuity product
    product_data = match_annuity_product(profile)
    product_name = product_data["recommended_product"]

    # Get product explanation
    explanation = explain_product(product_name)
    
    # Fetch available products for this customer profile
    products = fetch_annuity_products(profile["risk_tolerance"], product_name.lower())
    
    # Calculate estimated income (using $100k as example amount)
    income = calculate_annuity_income(int(profile["age"]), amount=100000)
    
    # Perform compliance check
    compliance = compliance_check(profile, product_name)

    # Format and return the recommendation
    return (
        f"💡 Recommendation: **{product_name}**\n"
        f"{explanation}\n\n"
        f"📦 Products matched: {[p['name'] for p in products]}\n"
        f"📊 Estimated income: ${income['monthly_income']}/mo for {income['years']} years\n"
        f"{compliance}"
    )
