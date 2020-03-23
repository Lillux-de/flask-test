from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return("Hello!!")

@app.route('/hello/')
@app.route('/hello/<string:name>')
def hello(name=None):
    resp = make_response(render_template('greet.html', name=name))
    resp.set_cookie('name', name)
    return resp

@app.route('/about')
def about():
    return 'This is a flask (python) test app.'