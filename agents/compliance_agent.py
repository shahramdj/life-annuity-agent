class ComplianceAgent:
    def check(self, profile, product):
        # Dummy compliance: ensure product matches risk profile
        if profile.get('risk') == 'low' and 'low risk' in [b.lower() for b in product.get('benefits', [])]:
            return True, "Product is suitable."
        elif profile.get('risk') == 'high':
            return True, "Product is suitable for high risk."
        return False, "Product does not match risk profile."
