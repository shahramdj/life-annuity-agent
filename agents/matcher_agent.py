import json

class MatcherAgent:
    def __init__(self, products_file):
        with open(products_file, 'r') as f:
            self.products = json.load(f)

    def match(self, profile):
        """Finds the best product(s) for a given profile."""
        scores = {}
        for product in self.products:
            score = 0
            profile_age = profile.get('age', 0)
            profile_risk = profile.get('risk', '').lower()
            profile_goals = profile.get('financial_goals', [])
            has_dependents = profile.get('dependents') # New

            # --- Scoring Logic ---
            # 1. Dependents Matching (New and Important)
            if product['type'] == 'life_insurance':
                if has_dependents:
                    score += 10 # Strongly recommend life insurance if user has dependents
                else:
                    score -= 10 # Penalize if no dependents
            
            # 2. Goal Matching
            if any(goal in product['suitable_for']['financial_goals'] for goal in profile_goals):
                score += 5
            else:
                score -= 20 # Disqualify if goals don't align

            # 3. Risk Matching
            if profile_risk == product['suitable_for']['risk_level']:
                score += 3
            elif (profile_risk == 'low' and product['suitable_for']['risk_level'] == 'medium') or \
                 (profile_risk == 'medium' and product['suitable_for']['risk_level'] == 'low'):
                score += 1
            elif profile_risk != product['suitable_for']['risk_level']:
                score -= 5

            # 4. Age Matching
            min_age, max_age = product['suitable_for']['age_range']
            if min_age <= profile_age <= max_age:
                score += 2
            else:
                score -= 20 # Disqualify if age is out of range
            
            scores[product['name']] = score
        
        if not scores:
            return []
        
        max_score = max(scores.values())
        return [prod for prod in self.products if scores[prod['name']] == max_score and max_score > 0]