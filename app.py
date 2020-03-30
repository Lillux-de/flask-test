from os import getenv #,urandom
from flask import Flask, render_template, request, make_response, session, escape, redirect, url_for, flash, get_flashed_messages, app, logging
import yeelight as yee

app = Flask(__name__)
app.secret_key = getenv('SESSION_KEY') #os.urandom(16) FIXME:


yeelight = {
	"id" : 0,
	"name" : "yeelight bulb",
	"ip" : "192.168.178.40",
	"bulb" : yee.Bulb("192.168.178.40"),
	"type" : "yeelight"
}
yeestrip = {
	"id" : 1,
	"name" : "yeelight strip",
	"ip" : "192.168.178.40",
	"bulb" : yee.Bulb("192.168.178.40"),
	"type" : "yeelight"
}
blinkstick = {
	"id" : 2,
	"name": "blinkstick",
	"ip" : "192.168.178.40",
	"bulb": None,
	"type" : "blinkstick"
}
lamps = [yeelight, yeestrip, blinkstick] #TODO: add blinkstick


@app.route('/')
def index():
	#TODO: wenn eingeloggt dann dashboard sonst login
	return redirect(url_for('dashboard') )


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html', lamps=lamps)


@app.route('/lamp/')
@app.route('/lamp/<int:lampid>', methods=['GET', 'POST'])
def lamp(lampid=None):
	if lampid == None:
		flash('please select a lamp from the dashboard first.', 'warning')
		return redirect(url_for('dashboard'))
	else:
		if request.method == 'POST':
			data = request.form
			lamps[lampid]['bulb'].set_rgb( int(data['r']) , int(data['g']) , int(data['b']) ) #TODO: switch case lamps[lampid].type for blinkstick and yeelight
			#print("r" + data['r'] + " g" + data['g'] + " b" + data['b'])
			return "got the data. thanks server."
		else:
			return render_template('lamp.html', lamp = lampid)


@app.route('/logout')
def logout():
	#remove username from session if its there
	session.pop('username', None)
	flash('successfull logout', 'success')
	return redirect(url_for('index'))


@app.route('/about')
def about():
	return render_template('about.html')