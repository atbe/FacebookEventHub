from ClubCrawler.Crawler import Crawler
import json

crawler = Crawler('config.json')

with open('club_events.json', 'w') as out:
	json_dump = json.dumps(crawler.clubs, default=lambda c: c.__dict__, sort_keys=True)
	print(json_dump, file=out)