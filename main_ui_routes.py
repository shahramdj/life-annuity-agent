from flask import Flask, send_from_directory
from main import app
import os

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), path)
