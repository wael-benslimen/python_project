from flask import render_template, redirect
from flask_app import app


@app.route('/')
def landing_page() :
    return render_template('landing_page.html')
