"""
mindfeed:

Heroku app to log entries from an rss/atom feed to beeminder
"""
import os
import time
import feedparser
from threading import Thread

from hammock import Hammock as BeeminderAPI


BEEMINDER_API_URL = os.environ.get('BEEMINDER_API_URL')
USERNAME = os.environ.get('USERNAME')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
GOAL = os.environ.get('GOAL')
FEED_URL = os.environ.get('FEED_URL')


beeminder = BeeminderAPI(BEEMINDER_API_URL)
datapoints = beeminder.users(USERNAME).goals(GOAL, 'datapoints.json')


def get_new_posts():
    print("Getting new posts")
    existing_datapoints = datapoints.GET(params={"auth_token": AUTH_TOKEN}).json()
    beeminder_links = set(point['comment'] for point in existing_datapoints)
    feed = feedparser.parse(FEED_URL)['entries']
    feed_links = set(entry['link'] for entry in feed)
    new_posts = feed_links - beeminder_links
    return new_posts


def create_new_datapoints(new_posts):
    for post in new_posts:
        print("Adding datapoint for:")
        print(post)
        datapoint = {
            "auth_token": AUTH_TOKEN,
            "value": 1,
            "comment": post
        }
        remote_datapoint = datapoints.POST(params=datapoint).json()
        for key in datapoint:
            if key != "auth_token":
                assert key in remote_datapoint
                assert datapoint[key] == remote_datapoint[key]


def main():
    print("Starting up...")
    while True:
        new_posts = get_new_posts()
        create_new_datapoints(new_posts)
        hours_remaining = 24
        while hours_remaining > 0:
            print("Sleeping for...")
            print(hours_remaining)
            print("...more hours.")
            time.sleep(60 * 60)
            hours_remaining = hours_remaining - 1


if __name__ == "__main__":
    main()
    