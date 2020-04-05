from os import getenv #,urandom
from flask import Flask, render_template, request, session, escape, redirect, url_for, flash, get_flashed_messages, app, jsonify
import yeelight as yee
import json

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
	"ip" : "192.168.178.35",
	"bulb" : yee.Bulb("192.168.178.35"),
	"type" : "yeelight"
}
blinkstick = {
	"id" : 2,
	"name": "blinkstick",
	"ip" : "localhost",
	"bulb": None,
	"type" : "blinkstick"
}
lamps = [yeelight, yeestrip, blinkstick]


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
			data = request.get_json()
			#print(data)
			lm = lamps[lampid]['bulb']

			#TODO: implement json logic analysis here, then call functions below.

			if 'color' in data:
				lm.set_rgb(  int(data['color']['r']) , int(data['color']['g']) , int(data['color']['b']) )
			if 'brightness' in data:
				lm.set_brightness( int(data['brightness']) )
			return "got the data. thanks server."
		else:
			return render_template('lamp.html', lamp = lampid)

def create_flow():
	pass

def change_color():
	pass

def change_brightness():
	pass


@app.route('/logout')
def logout():
	#remove username from session if its there
	session.pop('username', None)
	flash('successfull logout', 'success')
	return redirect(url_for('index'))


@app.route('/about')
def about():
	return render_template('about.html')