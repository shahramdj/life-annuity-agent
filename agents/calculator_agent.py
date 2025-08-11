class CalculatorAgent:
    def calculate_annuity_income(self, principal, rate, years):
        # Fixed annuity monthly payment calculation
        n = years * 12
        r = rate / 100 / 12
        print(f"[DEBUG] Calculating annuity income with principal={principal}, rate={rate}, years={years}, n={n}, r={r}")
        if r <= 0 or n <= 0:
            return 0
        payment = principal * r / (1 - (1 + r) ** -n)
        print(f"[DEBUG] Annuity monthly payment result: {payment}")
        return payment
