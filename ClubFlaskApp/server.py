import os
from flask import Flask
from flask import render_template
app = Flask(__name__)
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import subprocess
from ClubCrawler.Crawler import Crawler
import json

# sort the events by date, I'm sure this could be done on the client side
# and I'd probably prefer it be done there
events=[]

def load_events():
    print("called")
    global events
    events = []

    clubs =  get_latest_events_dict()
    for club in clubs:
        events += club['club_events']
    events.sort(key= lambda k: k['start_date_time'], reverse=True)

    # make the time stamps more readable
    for event in events:
        event['start_date_time'] = datetime.strptime(event['start_date_time'], '%Y-%m-%dT%H:%M:%S%z')
        event['date_time_str'] = event['start_date_time'].strftime('%A %B %d, %Y, at %I:%M%p')
        event['epoch'] = int(event['start_date_time'].timestamp())

def get_latest_events_dict():
    crawler = Crawler('config.json')
    json_dump = json.dumps(crawler.clubs, default=lambda c: c.__dict__, sort_keys=True)
    return json.loads(json_dump)

# single page web apps rock, tehe
@app.route('/')
def index():
    global events

    return render_template('index.html', events=events)

load_events() # initial load
scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=load_events,
    trigger=IntervalTrigger(seconds=1600), # update every half hour
    id='load_new_events',
    name='Loads the new events for the server to use.',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    load_events() # initial load
    app = Flask(__name__)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)