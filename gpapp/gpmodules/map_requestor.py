#! /usr/bin/env python
""" Module requesting the google maps API."""

import config
from urllib import request
import json


class MapRequestor :
    """Class which requests the google maps API."""

    def __init__(self, key_words):
        #self.key = config.GOOGLE_KEY
        self.key = "hsrh"
        self.key_words = key_words
        self.url = config.GOOGLE_MAPS_URL
        self.response = "   "
        self.longitude = 0
        self.latitude = 0

    def google_request(self):
        url = "".join([self.url, self.key_words, "&key=", self.key])
        response = request.urlopen(url)
        self.response = json.loads(response.read().decode("utf8"))
        print(self.response)
        self.response.longitude =
        self.response.latitude =
        self.response.addresss = 
