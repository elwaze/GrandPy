#! /usr/bin/env python
""" Module parsing the user's question to get keywords to insert in requests."""

import json
import re

class Parser:
    """Class which returns the keywords."""

    def __init__(self):
        """Loads filters contained in the 'stop_words.json' file"""
        with open('gpapp/gpmodules/stop_words.json') as file:
            stop_words = json.loads(file.read())
        self.stop_words = stop_words["stop_words"]
        self.punctuation_characters = stop_words["punctuation_characters"]
        self.location_words = stop_words["location_words"]
        self.re_punctuation = re.compile(
            '|'.join(map(re.escape, self.punctuation_characters))
        )

    def question_split(self, question):
        """Splits the question into a list of words"""
        question = str(question).lower()
        question = self.re_punctuation.split(question)
        question = [element for element in question if element != ""]
        return question

    def remove_stopwords(self, question):
        """Removes the useless stopwords contained in the 'stop_words.json file"""
        if not isinstance(question, (tuple, list, set)):
            raise TypeError('Question is not an iterable!')
        question = [word for word in question if word not in self.stop_words]
        return question

    def get_key_words(self, question):
        """Selects the useful information to be inserted in the requests"""
        if not isinstance(question, (tuple, list, set)):
            raise TypeError('Question is not an iterable!')

        question = ["," if word == "à" else word for word in question]
        request = '+'.join(question)
        for word in question:
            if word in self.location_words:
                index = question.index(word)
                request = '+'.join(question[index + 1:])
                break

        return request
