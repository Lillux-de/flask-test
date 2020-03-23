from os import getenv #,urandom
from flask import Flask, render_template, request, make_response, session, escape, redirect, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
import yeelight


app = Flask(__name__)
app.secret_key = getenv('SESSION_KEY') #os.urandom(16)
Bootstrap(app)

@app.route('/')
def index():
    if 'username' in session:
        return("Hello " + escape(session['username']))
    else:
        return redirect(url_for('login') )



@app.route('/dashboard')
def dashboard():

    yeelight = {
        "id" : 1,
        "name" : "yeelight bulb",
        "ip" : "192.168.178.40"
    }
    yeestrip = {
        "id" : 2,
        "name" : "yeelight strip",
        "ip" : "192.168.178.40"
    }
    lamps = [yeelight, yeestrip]
    
    return render_template('dashboard.html', lamps=lamps)

@app.route('/lamp/')
@app.route('/lamp/<int:lampid>')
def lamp(lampid):
    if lampid == None:
        return redirect(url_for('dashboard'))

    return render_template('lamp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('successfull login')
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    #remove username from session if its there
    session.pop('username', None)
    flash('successfull logout')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')