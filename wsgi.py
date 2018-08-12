from flask import Flask
from werkzeug.serving import run_simple
from __init__ import app as application

application = Flask(__name__)

if __name__ == "__main__":
    application.run()
run_simple('0.0.0.0', 8000, app, use_reloader=True)
