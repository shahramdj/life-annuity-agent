from flask import Flask, request, jsonify
from session_store import get_calc_session, set_calc_session, clear_calc_session
from agents.profiler_agent import ProfilerAgent
from agents.matcher_agent import MatcherAgent
from agents.calculator_agent import CalculatorAgent
from agents.calculator_session_agent import CalculatorSessionAgent
from agents.compliance_agent import ComplianceAgent
from agents.explainer_agent import ExplainerAgent
from agents.greeting_agent import GreetingAgent
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'  # Needed for Flask session

# Initialize agents
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), 'products', 'products.json')
profiler = ProfilerAgent()
matcher = MatcherAgent(PRODUCTS_FILE)
calculator = CalculatorAgent()
calc_session = CalculatorSessionAgent()
compliance = ComplianceAgent()
explainer = ExplainerAgent()
greeter = GreetingAgent()

# Simple in-memory session profile and state store
session_profiles = {}
session_states = {}

# Track which calculator parameter is being requested and their values
session_calculator_next = {}
session_calculator_params = {}

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json
    session_id = request.headers.get('X-Session-Id') or request.remote_addr
    msg = ''
    if isinstance(user_input, dict):
        msg = user_input.get('message', '')
    else:
        msg = str(user_input)

    # --- State machine ---
    # States: 'profiling', 'recommending', 'calculating', 'done'
    state = session_states.get(session_id, 'profiling')
    profile = session_profiles.get(session_id, {})
    response = {}

    # Greet on first message or new session
    if session_id not in session_states or (msg.strip().lower() in ["hi", "hello", "hey", "start"]):
        session_states[session_id] = 'profiling'
        session_profiles[session_id] = {}
        response['greeting'] = greeter.greet()
        return jsonify(response)

    # Detect restart or new profile info intent
    import re
    restart_phrases = ['restart', 'new product', 'start over', 'recommend again', 'new recommendation']
    has_restart = any(phrase in msg.lower() for phrase in restart_phrases)
    # Detect new profile info (age/risk)
    age_match = re.search(r'(?:age|i am|i\'m|aged)?\s*(\d{2})', msg, re.IGNORECASE)
    risk_match = re.search(r'(low risk|safe|conservative|high risk|aggressive|growth|medium risk|moderate)', msg, re.IGNORECASE)
    new_profile_info = (age_match or risk_match)
    if (has_restart or new_profile_info) and state != 'calculating':
        # Reset state to profiling and clear calculator session
        session_states[session_id] = 'profiling'
        calc_session.clear_session(session_id)
        # Optionally clear profile if explicit restart
        if has_restart:
            session_profiles[session_id] = {}
        state = 'profiling'

    # --- Corrected State Machine ---
    if state == 'profiling':
        # 1.1. Update profile with any new info
        profile = profiler.update_profile(msg, profile)
        session_profiles[session_id] = profile

        # 1.2. Check if profile is complete
        required_profile = ['age', 'risk', 'financial_goals', 'investment_amount']
        missing_profile = [k for k in required_profile if k not in profile]

        if missing_profile:
            # 1.3. If not complete, prompt for the next missing item
            prompts = {
                'age': 'To recommend the best product, may I know your age?',
                'risk': 'What is your risk tolerance? (low, medium, high)',
                'financial_goals': 'What is your main financial goal? (e.g., retirement income, protection, growth)',
                'investment_amount': 'How much do you plan to invest? (e.g., $10000)'
            }
            prompt = prompts[missing_profile[0]]
            response['profile_prompt'] = prompt
        else:
            # 1.4. If complete, transition to recommending state and continue
            session_states[session_id] = 'recommending'
            state = 'recommending'
    
    # NOTE: This is now an IF, allowing the state to fall through
    if state == 'recommending':
        # 2.1. Match profile to products
        print(f"[DEBUG] Product recommendation input profile: {profile}")
        matches = matcher.match(profile)
        results = []
        for product in matches:
            is_ok, compliance_msg = compliance.check(profile, product)
            if is_ok:
                explanation = explainer.explain(product)
                results.append({
                    'product': explanation,
                    'compliance': compliance_msg
                })
        
        if results:
            # 2.2. If matches found, recommend the first one
            recommended = results[0]
            session_profiles[session_id+'_recommended'] = recommended
            response['recommendation_msg'] = 'Based on your profile, I recommend the following product:'
            response['recommended_product'] = recommended
            response['profile'] = profile
            response['transition_msg'] = "Now, let's calculate your estimated monthly payment. I'll need a few details."

            # 2.3. Initialize calculator session
            calc_order = ['principal', 'rate', 'years']
            calc_params = {}
            if 'investment_amount' in profile:
                calc_params['principal'] = profile['investment_amount']
            set_calc_session(session_id, calc_params)

            # 2.4. Prompt for the first missing calculator parameter
            missing_calc_params = [p for p in calc_order if p not in calc_params]
            if missing_calc_params:
                next_param = missing_calc_params[0]
                prompts = {
                    'principal': 'What is the investment amount (principal)?',
                    'rate': 'What interest rate (%) should I use?',
                    'years': 'For how many years should I calculate the annuity?'
                }
                response['calculator_prompt'] = prompts[next_param]
                session_profiles[session_id+'_calc_next'] = next_param
                calc_session.set_last_requested(session_id, next_param)
            
            # 2.5. Transition state to calculating
            session_states[session_id] = 'calculating'
        else:
            # 2.6. If no matches, inform user and end session
            response['message'] = 'No suitable products found based on your profile. Please restart to try again.'
            session_states[session_id] = 'done'

    elif state == 'calculating':
        # 3.1. Extract calculator parameters from message
        params = get_calc_session(session_id)
        current_param = session_profiles.get(session_id+'_calc_next')
        val = None
        just_number = re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*', msg)

        if current_param:
            if just_number:
                val = just_number.group(1)
            else:
                extracted = calc_session.extract_params(msg, session_id=session_id)
                if current_param in extracted:
                    val = extracted[current_param]
            
            if val is not None:
                # 3.2. If a value was extracted, update the session
                if current_param == 'principal': params['principal'] = int(float(val))
                elif current_param == 'rate': params['rate'] = float(val)
                elif current_param == 'years': params['years'] = int(float(val))
                set_calc_session(session_id, params)
                print(f"[DEBUG] Updated calc params: {params}")

        # 3.3. Check if calculation is complete
        calc_order = ['principal', 'rate', 'years']
        missing_calc_params = [p for p in calc_order if p not in params]

        if not missing_calc_params:
            # 3.4. If complete, perform calculation
            print(f"[DEBUG] Performing annuity calculation with params: {params}")
            income = calculator.calculate_annuity_income(params['principal'], params['rate'], params['years'])
            response['calculator_result'] = f"Estimated monthly annuity payment: {income:.2f}"
            # 3.5. Transition to 'done' state and clear session
            session_states[session_id] = 'done'
            clear_calc_session(session_id)
            session_profiles.pop(session_id+'_recommended', None)
            session_profiles.pop(session_id+'_calc_next', None)
        else:
            # 3.6. If not complete, prompt for the next missing parameter
            next_param = missing_calc_params[0]
            prompts = {
                'principal': 'What is the investment amount (principal)?',
                'rate': 'What interest rate (%) should I use?',
                'years': 'For how many years should I calculate the annuity?'
            }
            response['calculator_prompt'] = prompts[next_param]
            session_profiles[session_id+'_calc_next'] = next_param
            calc_session.set_last_requested(session_id, next_param)

    elif state == 'done':
        # 4.1. Provide a closing message
        response['message'] = 'If you want to start a new recommendation, just let me know!'

    return jsonify(response)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    principal = data.get('principal', 0)
    rate = data.get('rate', 0)
    years = data.get('years', 0)
    income = calculator.calculate_annuity_income(principal, rate, years)
    return jsonify({'income': income})

if __name__ == '__main__':
    app.run(debug=True)
