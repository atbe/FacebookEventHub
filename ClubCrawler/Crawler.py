import facebook
import json
from pprint import pprint
import requests

"""

Spartan Hackers: bit.ly/cseSHmsu
ACM: fb.me/acmmsu
MSU Women in Computing: bit.ly/cseWICpage
SpartaSoft: bit.ly/cseSSpage
MSU Data Science: fb.me/MSUDataScience
Hackathon Hackers: bit.ly/hackHack

"""

DEBUG = True

class Crawler(object):

	def __init__(self, config_file_name):
		self.config = self.get_config(config_file_name)

		self.access_token = facebook.GraphAPI().get_app_access_token(
			app_id=self.config['api_auth']['client_id'],
			app_secret=self.config['api_auth']['client_secret']
		)
		self.api = facebook.GraphAPI(self.access_token)
		self.clubs = self.crawl_clubs(self.config['club_ids_to_crawl'])

	def get_config(self, config_file_name):
		return json.load(open(config_file_name))

	def crawl_clubs(self, club_ids):
		"""
		Builds the clubs using the id's,

		:param club_ids: An array of the id's to crawl.
		:return: Club objects build from the id's
		"""
		return [Club(id, self.api) for id in club_ids]

"""
Spartan Hackers Event Info:
	***Title*** : Intro to HTML / CSS
	Place and Time

	***Date/Time*** / ***Location*** : Sept. 12, 2016, 7 p.m. @ 233 Communication Arts Building

	Description

	Intro to HTML/CSS is the first workshop of the year hosted by Spartan Hackers. Drop by to learn some basics in web development, make connections, and eat pizza! **Make sure to bring your laptop**

"""

class Club(object):

	def __init__(self, id, api):
		self.id = id
		# self.graph_node = api.get_connections(id, connection_name='groups'
		self.graph_node = api.request(id.strip())
		if DEBUG:
			print(dir(self.graph_node))
			pprint(self.graph_node)

		self.club_events = self._go_collect_events(api)

		# input("Press enter to continue")

		self.name = self.graph_node['name']

	def _go_collect_events(self, api):
		events_json = api.request(self.id + '/events')
		if DEBUG:
			pprint(events_json)
			pprint(events_json.keys())

		# TODO: Club might not have 5, possible index error
		latest_5_events = [Event(event) for event in events_json['data']][:5]
		if DEBUG:
			print(latest_5_events)

		return latest_5_events

class Event(object):

	def __init__(self, event_json):
		self.name = event_json.get('name', None)
		self.start_date_time = event_json.get('start_time', None)
		self.end_date_time = event_json.get('end_time', None)
		self.id = event_json.get('id', None)
		self.location = event_json.get('location', None)
		self.timezone = event_json.get('timezone', None)
