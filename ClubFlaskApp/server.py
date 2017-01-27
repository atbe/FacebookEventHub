from flask import Flask
from flask import render_template
app = Flask(__name__)
import json
from datetime import datetime

events=[]
clubs =  json.load(open('../club_events.json'))
for club in clubs:
	events += club['club_events']
events.sort(key= lambda k: k['start_date_time'], reverse=True)
for event in events:
	event['start_date_time'] = datetime.strptime(event['start_date_time'], '%Y-%m-%dT%H:%M:%S%z').strftime(
		'%A %B %d, %Y, at %I:%M%p'
	)

@app.route('/')
def index():

	print("Serving", len(clubs), "clubs")

	return render_template('index.html', events=events)