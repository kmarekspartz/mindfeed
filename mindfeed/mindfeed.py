"""
mindfeed:

Heroku app to log entries from an rss/atom feed to beeminder
"""
import os
import time
from threading import Thread

import feedparser

from hammock import Hammock as BeeminderAPI

BEEMINDER_API_URL = os.environ.get('BEEMINDER_API_URL')
USERNAME = os.environ.get('USERNAME')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
GOAL = os.environ.get('GOAL')
FEED_URL = os.environ.get('FEED_URL')


beeminder = BeeminderAPI(BEEMINDER_API_URL)
datapoints = beeminder.users(USERNAME).goals(GOAL, 'datapoints.json')


def get_beeminder_links():
    print("Getting Beeminder links...")
    existing_datapoints = datapoints.GET(params={"auth_token": AUTH_TOKEN}).json()
    beeminder_links = set(point['comment'] for point in existing_datapoints)
    return beeminder_links


def get_feed_links():
    print("Getting feed links...")
    feed = feedparser.parse(FEED_URL)['entries']
    feed_links = set(entry['link'] for entry in feed)
    return feed_links


def get_new_posts():
    beeminder_links = get_beeminder_links()
    feed_links = get_feed_links()
    new_posts = feed_links - beeminder_links
    return new_posts


def create_new_datapoints(new_posts):
    for post in new_posts:
        print("Adding datapoint for: {0}".format(post))
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
            print("Sleeping for {0} more hours.".format(hours_remaining))
            time.sleep(60 * 60)
            hours_remaining = hours_remaining - 1
