import re

class ProfilerAgent:
    def __init__(self):
        """
        A stateless agent that extracts profile information from a message.
        """
        pass

    def update_profile(self, msg, current_profile):
        """
        Updates a given profile dictionary with information extracted from a message.
        It does not store any state itself.
        """
        profile = current_profile.copy()

        # Extract age
        age_match = re.search(r'\b(\d{1,2})\b', msg, re.IGNORECASE)
        if age_match:
            profile['age'] = int(age_match.group(1))

        # Extract risk tolerance
        risk_match = re.search(r'(low|medium|high)\s*risk', msg, re.IGNORECASE)
        if not risk_match:
            risk_match = re.search(r'\b(low|medium|high)\b', msg, re.IGNORECASE)
        if risk_match:
            profile['risk'] = risk_match.group(1).lower()

        # Financial goals
        goals_match = re.search(r'(retirement|income|protection|growth)', msg, re.IGNORECASE)
        if goals_match:
            goal = goals_match.group(1).lower()
            if 'retirement' in goal or 'income' in goal:
                profile['financial_goals'] = ['retirement income']
            elif 'protection' in goal:
                profile['financial_goals'] = ['protection']
            elif 'growth' in goal:
                profile['financial_goals'] = ['growth']
        
        # Extract dependents info
        dependents_match = re.search(r'\b(yes|no|i do|i don\'t)\b', msg, re.IGNORECASE)
        if dependents_match:
            answer = dependents_match.group(1).lower()
            if answer in ['yes', 'i do']:
                profile['dependents'] = True
            elif answer in ['no', 'i don\'t']:
                profile['dependents'] = False

        # Extract investment amount
        amt_match = re.search(r'(?:\$|amount|invest|investment)\s*([\d,]+)', msg, re.IGNORECASE)
        if amt_match:
            amount_str = amt_match.group(1).replace(',', '')
            profile['investment_amount'] = int(amount_str)

        return profile