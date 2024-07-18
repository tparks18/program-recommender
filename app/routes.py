from app import app
from flask import redirect, url_for, render_template


@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title=title)

@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html', title=title)

@app.route('/resources')
def resources():
    title = 'Resources'
    return render_template('resources.html', title=title)