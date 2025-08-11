#!C:\Users\2189005\AppData\Local\Microsoft\WindowsApps\python.exe
# To run this, use your python path explicitly if needed:
# "C:\Users\2189005\AppData\Local\Microsoft\WindowsApps\python.exe" test_calculator_flow.py

import requests

def test_calculator_flow():
    session = requests.Session()
    url = 'http://127.0.0.1:5000/chat'
    headers = {'Content-Type': 'application/json'}
    # Simulate the full chat flow
    def post(msg):
        r = session.post(url, json={'message': msg, 'session_id': 'test123'}, headers=headers)
        print(f'User: {msg}')
        print(f'Bot: {r.json()}')
        return r.json()

    # 1. Greet
    post('hi')
    # 2. Provide age
    post('I am 78')
    # 3. Provide risk
    post('low')
    # 4. Provide financial goal
    post('growth')
    # 5. Provide investment amount
    post('$2000000')
    # 6. Should recommend product and ask for rate
    post('8')
    # 7. Should ask for years
    post('20')
    # 8. Should calculate and show payment

if __name__ == '__main__':
    test_calculator_flow()
