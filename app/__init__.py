from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret_key_not_important_here'

from app import routes
