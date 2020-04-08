#! /usr/bin/env python
""" Module requesting the wikipedia API."""

import config
import requests


class WikiRequestor:
    """Class which requests the wikipedia API."""

    def __init__(self, geometry):
        # self.key_words = key_words
        self.geometry = geometry
        self.url = config.WIKIPEDIA_URL

    def wiki_request(self, url):
        """
        Initial request of Wiki API.
        :param url: url for the request
        :return: response received from thi API.
        """

        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()
        data = response.json()

        return data['query'], 200

    def page_id_search(self):
        """
        Calls wiki_request() with the needed parameters
        to get the page_id and the title of the wanted page.
        :return: dictionary with the page_id and the page title.
        """
        geo_request = f"{self.url}&list=geosearch&gsradius=5000" \
                      f"&gslimit=1&gscoord={self.geometry}"
        result, code = self.wiki_request(geo_request)
        result = result['geosearch']

        page_id = result[0]['pageid']
        title = result[0]['title']

        result = dict(
            page_id=page_id,
            title=title,
        )
        return result, 200

    def extract(self):
        """
        Wiki API request to get the extract of the wanted page.
        Uses the page_id get by page_id_search() to call wiki_request().
        :return: page_id_search result updated with the returned extract.
        """
        # getting the page id
        data, code = self.page_id_search()
        page_id = data['page_id']
        extract_request = f"{self.url}&exintro=1&explaintext" \
                          f"=1&exsentences=2&pageids={page_id}"
        # getting the extract
        result, code = self.wiki_request(extract_request)
        extract = result['pages'][f'{page_id}']['extract']
        data.update({"extract": extract})

        return data, 200
