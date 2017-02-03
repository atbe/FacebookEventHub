import os
from flask import Flask
from flask import render_template
app = Flask(__name__)
import json
from datetime import datetime

# sort the events by date, I'm sure this could be done on the client side
# and I'd probably prefer it be done there
events=[]
clubs =  json.load(open('./club_events.json'))
for club in clubs:
    events += club['club_events']
events.sort(key= lambda k: k['start_date_time'], reverse=True)

# make the time stamps more readable
for event in events:
    event['start_date_time'] = datetime.strptime(event['start_date_time'], '%Y-%m-%dT%H:%M:%S%z')
    event['date_time_str'] = event['start_date_time'].strftime('%A %B %d, %Y, at %I:%M%p')
    event['epoch'] = int(event['start_date_time'].timestamp())

# single page web apps rock, tehe
@app.route('/')
def index():
    return render_template('index.html', events=events)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
