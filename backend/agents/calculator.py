def calculate_annuity_income(age: int, amount: float, rate: float = 0.05, years: int = 20) -> dict:
    """
    Calculate annuity income based on age, amount, rate, and years.
    Returns monthly income, total income, and years.
    """
    annual_income = amount * rate
    return {
        "monthly_income": round(annual_income / 12, 2),
        "total_income": round(annual_income * years, 2),
        "years": years
    }
