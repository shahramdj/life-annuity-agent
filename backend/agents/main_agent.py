from cursor import agent
from agents.profiler import profile_customer
from agents.matcher import match_annuity_product, fetch_annuity_products
from agents.calculator import calculate_annuity_income
from agents.explainer import explain_product
from agents.compliance import compliance_check

@agent
def annuity_recommendation_agent(conversation: str) -> str:
    profile = profile_customer(conversation)
    product_data = match_annuity_product(profile)
    product_name = product_data["recommended_product"]

    explanation = explain_product(product_name)
    products = fetch_annuity_products(profile["risk_tolerance"], product_name.lower())
    income = calculate_annuity_income(int(profile["age"]), amount=100000)
    compliance = compliance_check(profile, product_name)

    return (
        f"💡 Recommendation: **{product_name}**\n"
        f"{explanation}\n\n"
        f"📦 Products matched: {[p['name'] for p in products]}\n"
        f"📊 Estimated income: ${income['monthly_income']}/mo for {income['years']} years\n"
        f"{compliance}"
    )
