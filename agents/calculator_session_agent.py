import re

class CalculatorSessionAgent:
    def __init__(self):
        self.sessions = {}  # session_id -> param dict
        self.last_requested = {}  # session_id -> last missing param

    def extract_params(self, message, session_id=None):
        # Try to extract principal, rate, years from message
        params = {}
        # Principal (look for $ or numbers with 'invest', 'amount', etc.)
        principal_match = re.search(r'(?:\$|invest|amount|principal)[^\d]*(\d+[\d,]*)', message, re.IGNORECASE)
        if principal_match:
            params['principal'] = int(principal_match.group(1).replace(',', ''))
        # Rate (robust: match any number, with or without %, with or without 'rate', or just a number)
        rate_match = re.search(r'(?:rate[^\d]*)?(\d+(?:\.\d+)?)\s*%?', message, re.IGNORECASE)
        if rate_match:
            params['rate'] = float(rate_match.group(1))
        # Years (robust: match '20', '20 years', '20yrs', 'for 20 years', etc.)
        years_match = re.search(r'(?:for\s*)?(\d+)\s*(?:years|yrs|year)?', message, re.IGNORECASE)
        if years_match:
            params['years'] = int(years_match.group(1))
        # If no context, but a number is given and we know which param we're asking for
        if session_id:
            just_number = re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*', message)
            if just_number and not params:
                last = self.last_requested.get(session_id)
                if last == 'principal':
                    params['principal'] = int(float(just_number.group(1)))
                elif last == 'rate':
                    params['rate'] = float(just_number.group(1))
                elif last == 'years':
                    params['years'] = int(float(just_number.group(1)))
        return params

    def get_missing(self, params):
        missing = []
        for k in ['principal', 'rate', 'years']:
            if k not in params:
                missing.append(k)
        return missing

    def set_last_requested(self, session_id, param):
        self.last_requested[session_id] = param

    def get_last_requested(self, session_id):
        return self.last_requested.get(session_id)

    def update_session(self, session_id, params):
        session = self.sessions.setdefault(session_id, {})
        session.update(params)
        return session

    def clear_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session(self, session_id):
        return self.sessions.get(session_id, {})
