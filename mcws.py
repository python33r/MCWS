# -*- coding: utf-8 -*-
"""
Tools for working with JRiver Media Core Web Services (MCWS).
"""

import requests
from xml.etree import ElementTree as et
from datetime import datetime


URLS = {
    "check_service" : "http://{}:52199/MCWS/v1/Alive",
    "now_playing"   : "http://{}:52199/MCWS/v1/Playback/Info?Zone=-1",
    "played_tracks" : "http://{}:52199/MCWS/v1/Files/Search"
}


class ServiceException(Exception):
    pass


class Service:
    """
    Simple abstraction of JRiver MCWS.
    """

    def __init__(self, address):
        self.address = address
        for name, url_template in URLS.items():
            self.urls[name] = url_template.format(address)

    def _get_response(self, name):
        try:
            http_response = requests.get(self.urls[name])
            response = et.fromstring(http_response.content)
            if response.get("Status") != "OK":
                raise ServiceException("Status not OK")
            return response
        except:
            raise ServiceException("Cannot access MCWS")

    def get_now_playing(self):
        response = self._get_response("now_playing")

        elapsed = response.find("Item[@Name='ElapsedTimeDisplay']")
        remaining = response.find("Item[@Name='RemainingTimeDisplay']")
        artist = response.find("Item[@Name='Artist']")
        album = response.find("Item[@Name='Album']")
        track = response.find("Item[@Name='Name']")
        status = response.find("Item[@Name='Status']")

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
        response = self._get_response("played_tracks")
        items = response.findall("Item/Field[@Name='Number Plays']/..")

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
