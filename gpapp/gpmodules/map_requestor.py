#! /usr/bin/env python
""" Module requesting the google maps API."""

import config
import requests


class MapRequestor :
    """Class which requests the google maps API."""

    @property
    def url(self):
        return "".join([self.maps_url, self.key_words, "&key=", self.key])

    def __init__(self, key_words):
        self.key = config.GOOGLE_KEY
        self.key_words = key_words
        self.maps_url = config.GOOGLE_MAPS_URL

    def google_request(self):

        response = requests.get(self.url)
        if not response.ok:
            response.raise_for_status()

        data = response.json()
        status = data['status']

        if status == "OK":
            result = dict(
                status=status,
                address=data['results'][0]['formatted_address'],
                latitude=data['results'][0]['geometry']['location']['lat'],
                longitude=data['results'][0]['geometry']['location']['lng'],
            )
        else:
            result = dict(
                status=status,
                message=data.get('error_message', 'unknown issue'),
            )

        return result, 200
