# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 23:20:26 2015

@author: Nick Efford
"""

import requests
from xml.etree import ElementTree as et
from datetime import datetime

URL = "http://{}:52199/MCWS/v1/Files/Search"


def get_played_tracks(server):

    # Obtain file details via MCWS

    response = requests.get(URL.format(server))
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


if __name__ == "__main__":
    from configparser import ConfigParser
    config = ConfigParser()
    config.read("mcws.config")

    tracks = get_played_tracks(config["server"]["address"])

    for track in tracks:
        print("{}, {}: plays={}, last at {}".format(
          track["artist"], track["title"], track["plays"], track["last"]))
