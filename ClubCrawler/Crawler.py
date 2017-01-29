import facebook
import json
from pprint import pprint
import requests
from datetime import datetime
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
		return [Club(id, self.api, int(self.config['number_of_events'])) for id in club_ids]

"""
Spartan Hackers Event Info:
	***Title*** : Intro to HTML / CSS
	Place and Time

	***Date/Time*** / ***Location*** : Sept. 12, 2016, 7 p.m. @ 233 Communication Arts Building

	Description

	Intro to HTML/CSS is the first workshop of the year hosted by Spartan Hackers. Drop by to learn some basics in web development, make connections, and eat pizza! **Make sure to bring your laptop**

"""

class Club(object):

	def __init__(self, group_name_id, api, number_of_events):
		self.group_name_id = group_name_id.strip()
		graph_node = api.request(self.group_name_id)
		if DEBUG:
			print('graph_node=', graph_node)

		self.name = graph_node['name']
		self.id = graph_node['id']

		self.cover_image_url = self._go_collect_cover_image(api)
		self.club_events = self._go_collect_events(api, number_of_events)

	def _go_collect_cover_image(self, api):
		# without redict=false, request would return raw image data
		group_image_graph_node = api.request('{}/picture/'.format(self.id),
		                                     args={'height': 250, 'type': 'square', 'access_token': api.access_token, 'redirect': 'false'})
		return group_image_graph_node['data']['url']

	def _go_collect_events(self, api, number_of_events):
		events_json = api.request(self.group_name_id + '/events')
		if DEBUG:
			pprint(events_json)
			pprint(events_json.keys())

		# TODO: Club might not have 5, possible index error
		events_json['data'].sort(key=lambda k: k['start_time'], reverse=True)
		latest_5_events = [Event(event, self.name, self.group_name_id, self.cover_image_url, api) for event in events_json['data']][:number_of_events]
		if DEBUG:
			print(latest_5_events)

		return latest_5_events

class Event(object):

	def __init__(self, event_json, club_name, club_id, club_cover_image_url, api):
		self.name = event_json.get('name', None)
		self.start_date_time = event_json.get('start_time', None)
		self.end_date_time = event_json.get('end_time', None)
		self.id = event_json.get('id', None)
		self.place = event_json.get('place', None)
		self.timezone = event_json.get('timezone', None)
		self.description = event_json.get('description', None)
		self.club_name = club_name
		self.club_id = club_id
		self.club_cover_image_url = club_cover_image_url