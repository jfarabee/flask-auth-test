"""
The flask application package.
"""

from flask import Flask
from flask_restful import Api
import flask_auth_test.api

app = Flask(__name__)
api = Api(app)

# Entry point for log, HTTP req handlers in api.py
api.add_resource(api.Log, '/api/log')
# Entry point for email, HTTP req handlers in api.py
api.add_resource(api.Email, '/api/email')

import flask_auth_test.views
