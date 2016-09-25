from flask import Flask


app = Flask(__name__)
app.secret_key = 'NewBisPassword(%@&'


from app import views