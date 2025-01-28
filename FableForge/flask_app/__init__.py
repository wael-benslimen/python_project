from flask import Flask
app = Flask(__name__)
app.secret_key = "secret_key"
DB  = "fable_forge_schema"
