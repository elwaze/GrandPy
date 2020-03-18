#! /usr/bin/env python

import os
import json
import requests
import unittest
import unittest.mock as mock
from io import BytesIO
from gpapp.gpmodules.parser import Parser
from gpapp.gpmodules.map_requestor import MapRequestor
from gpapp.gpmodules.wiki_requestor import WikiRequestor


class TestParser:
    """Class for tests of functions contained in module parser.py"""
    def setup(self):
        """Setup for the parser tests"""
        self.parser = Parser()
        self.questions = [
            ("dis, grand-py, tu peux me donner l'adresse de la Tour Eiffel ?",
             ["dis", "grand-py", "tu", "peux", "me", "donner", "l", "adresse", "de", "la", "tour", "eiffel"],
             ["dis", "grand-py", "donner", "adresse", "tour", "eiffel"],
             "tour+eiffel"),
            ("Salut pépé ! Où je peux trouver le parc de la tête d'or à Lyon ?",
             ["salut", "pépé", "où", "je", "peux", "trouver", "le", "parc", "de", "la", "tête", "d", "or", "à", "lyon"],
             ["salut", "pépé", "où", "trouver", "parc", "tête", "or", "à", "lyon"],
             "parc+tête+or+,+lyon")
        ]

    def test_split_question(self):
        """Checks that the question_split function returns a list of words"""

        # calling function
        for question in self.questions:
            result = self.parser.question_split(question[0])
            # expected result
            assert result == question[1]

    def test_question_cleaned(self):
        """Checks that remove_stopwords() returns a list of words not in the stopwords"""

        # calling function
        for question in self.questions:
            result = self.parser.remove_stopwords(question[1])
            # expected result
            assert result == question[2]

    def test_get_key_words(self):
        """Checks that get_key_words() returns only the useful words"""

        # calling function
        for question in self.questions:
            result = self.parser.get_key_words(question[2])
            # expected result
            assert result == question[3]


class TestMap(unittest.TestCase):
    """Class for tests of functions contained in module map_requestor.py"""
    def setUp(self):
        """Setup for the google maps requestor tests"""
        os.environ['GOOGLE_API_KEY'] = 'testouille de la grenouille'
        self.requestor = MapRequestor("tour+eiffel")

    def _setup_mocked_response(self, response, ok_status=True):
        mocked_response = mock.Mock(ok=ok_status)
        mocked_response.json.return_value = response
        return mocked_response

    @mock.patch('requests.get')
    def test_api_request_ok(self, mocked_requests_get):
        expected_result = {
            "results": [
                {
                    "formatted_address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris",
                    "geometry": {
                        "location": {
                            "lat": 48.85837,
                            "lng": 2.94481
                        }
                    }
                }
            ],
            "status": "OK"
        }
        mocked_response = self._setup_mocked_response(expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.google_request()
        # expected result

        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            status=expected_result['status'],
            address=expected_result['results'][0]['formatted_address'],
            latitude=expected_result['results'][0]['geometry']['location']['lat'],
            longitude=expected_result['results'][0]['geometry']['location']['lng'],
        ))

    @mock.patch('requests.get')
    def test_api_request_error(self, mocked_requests_get):

        expected_result = {
            "results": [],
            "status": "ERROR",
            "message": 'unknown issue'
        }

        mocked_response = self._setup_mocked_response(expected_result, ok_status=False)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.google_request()

        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            status=expected_result['status'],
            message=expected_result['message']
        ))


class TestWiki(unittest.TestCase):
    """Class for tests of functions contained in module wiki_requestor.py"""

    def setUp(self):
        """Setup for the wikipedia requestor tests"""
        geometry = '48.85837|2.294481'
        key_words = 'tour+eiffel'
        self.url_ask = "fake url for test"
        self.requestor = WikiRequestor(geometry, key_words)
        self.expected_result = {
            "query": {
                "pages": {
                    1359783: {
                        "pageid": 1359783,
                        "ns": 0,
                        "title": "Tour Eiffel",
                        "extract": "La tour Eiffel est une tour de fer puddlé de 324 mètres de hauteur (avec antennes) "
                                   "située à Paris, à l’extrémité nord-ouest du parc du Champ-de-Mars en bordure de la "
                                   "Seine dans le 7e arrondissement. Son adresse officielle est 5, avenue Anatole-France."
                    }
                }
            }
        }


    def _setup_mocked_response(self, response):
        mocked_response = mock.Mock()
        mocked_response.json.return_value = response
        return mocked_response

    @mock.patch('requests.get')
    def test_wiki_request_ok(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))

    @mock.patch('requests.get')
    def test_wiki_request_error(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))

    @mock.patch('requests.get')
    def page_id_search_ok(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))

    @mock.patch('requests.get')
    def page_id_search_error(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))

    @mock.patch('requests.get')
    def extract_ok(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))
    @mock.patch('requests.get')
    def extract_error(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response(self.expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.requestor.url)

        self.assertDictEqual(response, dict(
            #title=self.expected_result['query']['pages'][1359783]['title'],
            #extract=self.expected_result['query']['pages'][1359783]['extract']
        ))
