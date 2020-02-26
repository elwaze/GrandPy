#! /usr/bin/env python
""" Module parsing the user's question to get keywords to insert in requests."""

import json


class Parser:
    """Class which returns the keywords."""

    def __init__(self):
        """Loads filters contained in the 'stop_words.json' file"""
        with open('stop_words.json') as file:
            stop_words = json.loads(file.read())
        self.stop_words = stop_words["stop_words"]

    def split(self, question):
        """Splits the question into a list of words"""

    def remove_stopwords(self, question):
        """Removes the useless stopwords contained in the 'stop_words.json file"""

    def get_key_words(self, question):
        """Selects the useful information to be inserted in the requests"""
