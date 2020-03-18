#! /usr/bin/env python
""" Module requesting the wikipedia API."""

import config
import requests


class WikiRequestor :
    """Class which requests the wikipedia API."""

    def __init__(self, geometry, key_words):
        self.key_words = key_words
        self.geometry = geometry
        self.url = config.WIKIPEDIA_URL

    def wiki_request(self, ask):
        """
        Initial request of Wiki API.
        :param ask: url for the request
        (depending if it's a request by key words or by geolocation).
        :return: response received from thi API.
        """

        response = requests.get(ask)
        if not response.ok:
            response.raise_for_status()

        response = response['query']
        data = response.json()
        return data, 200

    def page_id_search(self):
        """
        Calls wiki_request() with the needed parameters to get the page_id and the title of the wanted page.
        :return: dictionary with the page_id, the page title and the "mode"
        ("exact" = page = place wanted ; "nearby" = closest place from the place wanted).
        """

        kw_request = self.url + "&list=search&srlimit=1&srsearch=" + self.key_words
        result, code = self.wiki_request(kw_request)
        result = result['search']
        mode = "exact"
        if not result:
            geo_request = self.url + "&list=geosearch&gsradius=5000&gslimit=1&gscoord=" + self.geometry
            result, code = self.wiki_request(geo_request)
            result = result['geosearch']
            mode = "nearby"

        page_id = result[0]['pageid']
        title = result[0]['title']

        result = dict(
            page_id=page_id,
            title=title,
            mode=mode
        )
        return result, 200

    def extract(self):
        """
        Wiki API request to get the extract of the wanted page.
        Uses the page_id get by page_id_search() to call wiki_request().
        :return: page_id_search result updated with the returned extract.
        """
        data, code = self.page_id_search()
        extract_request = self.url + "&exintro=1&explaintext=1&exsentences=2&pageids=" + data['page_id']
        result, code = self.wiki_request(extract_request)
        extract = result['pages'][data['page_id']]['extract']
        data.update({"extract": extract})

        return data, 200
