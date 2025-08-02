from cursor import tool

@tool
def calculate_annuity_income(age: int, amount: float, rate: float = 0.05, years: int = 20) -> dict:
    annual_income = amount * rate
    return {
        "monthly_income": round(annual_income / 12, 2),
        "total_income": round(annual_income * years, 2),
        "years": years
    }
