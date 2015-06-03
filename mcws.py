# -*- coding: utf-8 -*-
"""
Tools for working with JRiver Media Center Web Services (MCWS).
"""

import requests
from xml.etree import ElementTree as et
from datetime import datetime


class Service:

    CHECK_SERVICE = "http://{}:52199/MCWS/v1/Alive"
    NOW_PLAYING = "http://{}:52199/MCWS/v1/Playback/Info?Zone=-1"
    PLAYED_TRACKS = "http://{}:52199/MCWS/v1/Files/Search"

    def __init__(self, address):
        self.address = address
        url = self.CHECK_SERVICE.format(self.address)
        try:
            response = requests.get(url)
            root = et.fromstring(response.content)
            if root.get("Status") == "OK":
                self.is_running = True
            else:
                self.is_running = False
        except:
            self.is_running = False

    def get_now_playing(self):
        url = self.NOW_PLAYING.format(self.address)
        response = requests.get(url)
        root = et.fromstring(response.content)
        if root.get("Status") != "OK":
            return None

        elapsed = root.find("Item[@Name='ElapsedTimeDisplay']")
        remaining = root.find("Item[@Name='RemainingTimeDisplay']")
        artist = root.find("Item[@Name='Artist']")
        album = root.find("Item[@Name='Album']")
        track = root.find("Item[@Name='Name']")
        status = root.find("Item[@Name='Status']")

        details = {
          "elapsed": elapsed.text,
          "remaining": remaining.text,
          "artist": artist.text,
          "album": album.text,
          "track": track.text
        }

        if status is not None:
            details["status"] = status.text

        return details

    def get_played_tracks(self):
        url = self.PLAYED_TRACKS.format(self.address)
        response = requests.get(url)
        root = et.fromstring(response.content)

        items = root.findall("Item/Field[@Name='Number Plays']/..")

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
