from os import getenv #,urandom
from flask import Flask, render_template, request, make_response, session, escape, redirect, url_for, flash, get_flashed_messages, app, logging
from flask_bootstrap import Bootstrap
import yeelight as yee

app = Flask(__name__)
app.secret_key = getenv('SESSION_KEY') #os.urandom(16)
Bootstrap(app)

yeelight = {
    "id" : 0,
    "name" : "yeelight bulb",
    "ip" : "192.168.178.40"
}
yeestrip = {
    "id" : 1,
    "name" : "yeelight strip",
    "ip" : "192.168.178.40"
}
lamps = [yeelight, yeestrip]

bulb = yee.Bulb("192.168.178.40")
bulb.turn_on()
bulb.set_rgb(255,255,255)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard') )
    else:
        return redirect(url_for('login') )


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', lamps=lamps)


@app.route('/lamp/')
@app.route('/lamp/<int:lampid>', methods=['GET', 'POST'])
def lamp(lampid=None):
    if lampid == None:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            data = request.form
            bulb.set_brightness( int(data['a']) * 100)
            bulb.set_rgb( int(data['r']) , int(data['g']) , int(data['b']) )
#            print("r" + data['r'] + " g" + data['g'] + " b" + data['b'])
            return "got the data. thanks server."
        else:
            #bulb = yee.Bulb(lamps[lampid].ip)
            return render_template('lamp.html', lamp = lampid)



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