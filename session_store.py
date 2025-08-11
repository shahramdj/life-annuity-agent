import json
import os

SESSION_FILE = os.path.join(os.path.dirname(__file__), 'calc_sessions.json')

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_sessions(sessions):
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f)

def get_calc_session(session_id):
    sessions = load_sessions()
    return sessions.get(session_id, {})

def set_calc_session(session_id, params):
    sessions = load_sessions()
    sessions[session_id] = params
    save_sessions(sessions)

def clear_calc_session(session_id):
    sessions = load_sessions()
    if session_id in sessions:
        del sessions[session_id]
        save_sessions(sessions)
