# -*- coding: utf-8 -*-
"""
Tools for working with JRiver Media Core Web Services (MCWS).
"""

import requests
from xml.etree import ElementTree as et
from datetime import datetime


URLS = {
    "alive"       : "http://{}:52199/MCWS/v1/Alive",
    "artists"     : "http://{}:52199/MCWS/v1/Library/Values?Field=Artist",
    "tracks"      : "http://{}:52199/MCWS/v1/Files/Search?Fields=Artist,Album,Name,Number%20Plays,Last%20Played",
    "now_playing" : "http://{}:52199/MCWS/v1/Playback/Info?Zone=-1",
}


class ServiceException(Exception):
    pass


class Service:
    """
    Simple abstraction of JRiver MCWS.
    """

    def __init__(self, address):
        self.address = address
        self.urls = {}
        for name, url_template in URLS.items():
            self.urls[name] = url_template.format(address)

    def _get_response(self, name):
        try:
            response = requests.get(self.urls[name])
            return et.fromstring(response.content)
        except:
            raise ServiceException("Cannot access MCWS")

    def get_artists(self):
        response = self._get_response("artists")
        if response.get("Status") != "OK":
            raise ServiceException("Status not OK")

        artists = response.findall("Item")
        return [ artist.text for artist in artists ]

    def get_now_playing(self):
        response = self._get_response("now_playing")
        if response.get("Status") != "OK":
            raise ServiceException("Status not OK")

        status = response.find("Item[@Name='Status']")
        if status is None:
            return None
        elif status.text == "Playing":
            artist = response.find("Item[@Name='Artist']")
            album = response.find("Item[@Name='Album']")
            title = response.find("Item[@Name='Name']")
            elapsed = response.find("Item[@Name='ElapsedTimeDisplay']")
            remaining = response.find("Item[@Name='RemainingTimeDisplay']")
            return {
              "artist": artist.text,
              "album": album.text,
              "title": title.text,
              "elapsed": elapsed.text,
              "remaining": remaining.text
            }
        else:
            return None

    def get_played_tracks(self):
        response = self._get_response("tracks")
        items = response.findall("Item/Field[@Name='Number Plays']/..")

        data = []
        for item in items:
            artist = item.find("Field[@Name='Artist']")
            album = item.find("Field[@Name='Album']")
            title = item.find("Field[@Name='Name']")
            num_plays = item.find("Field[@Name='Number Plays']")
            last_played = item.find("Field[@Name='Last Played']")
            data.append({
              "artist" : artist.text,
              "album"  : album.text,
              "title"  : title.text,
              "plays"  : int(num_plays.text),
              "last"   : datetime.fromtimestamp(int(last_played.text))
            })

        return data
