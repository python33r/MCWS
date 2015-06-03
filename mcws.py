# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 23:20:26 2015

@author: Nick Efford
"""

import requests
from xml.etree import ElementTree as et
from datetime import datetime


class Server:

    NOW_PLAYING_URL = "http://{}:52199/MCWS/v1/Playback/Info?Zone=-1"
    PLAYED_TRACKS_URL = "http://{}:52199/MCWS/v1/Files/Search"

    def __init__(self, address):
        self.address = address

    def get_now_playing(self):
        url = self.NOW_PLAYING_URL.format(self.address)
        response = requests.get(url)
        root = et.fromstring(response.content)

        elapsed = root.find("Item[@Name='ElapsedTimeDisplay']")
        remaining = root.find("Item[@Name='RemainingTimeDisplay']")
        artist = root.find("Item[@Name='Artist']")
        album = root.find("Item[@Name='Album']")
        track = root.find("Item[@Name='Name']")
        status = root.find("Item[@Name='Status']")

        return {
          "status": status.text,
          "elapsed": elapsed.text,
          "remaining": remaining.text,
          "artist": artist.text,
          "album": album.text,
          "track": track.text
        }

    def get_played_tracks(self):
        url = self.PLAYED_TRACKS_URL.format(self.address)
        response = requests.get(url)
        root = et.fromstring(response.content)

        # Find all returned items with a 'Number Plays' field

        items = root.findall("Item/Field[@Name='Number Plays']/..")

        # Extract relevant details from each item

        data = []
        for item in items:
            artist = item.find("Field[@Name='Artist']")
            album = item.find("Field[@Name='Album']")
            track = item.find("Field[@Name='Name']")
            num_plays = item.find("Field[@Name='Number Plays']")
            last_played = item.find("Field[@Name='Last Played']")
            data.append({
              "artist" : artist.text,
              "album"  : album.text,
              "title"  : track.text,
              "plays"  : int(num_plays.text),
              "last"   : datetime.fromtimestamp(int(last_played.text))
            })

        return data
