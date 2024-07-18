from app import app
from flask import redirect, url_for, render_template


@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title=title)
