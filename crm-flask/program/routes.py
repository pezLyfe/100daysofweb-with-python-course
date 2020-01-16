from program import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html')

@app.route('/100Days')
def p100Days():
        return render_template('100days.html')

@app.route('/cast')
def cast():
        return render_template('cast.html')

@app.route('/mission')
def mission():
        return render_template('mission.html')

@app.route('/shows')
def shows():
        return render_template('shows.html')