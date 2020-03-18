#! /usr/bin/env python

import os
import json
import requests
import unittest
import unittest.mock as mock
from io import BytesIO

import config
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

    def _setup_mocked_response(self, response, **options):
        magic = options.pop('magic', False)
        if magic:
            mocked_response = mock.MagicMock(**options)
        else:
            mocked_response = mock.Mock(**options)
        mocked_response.json.return_value = response
        return mocked_response

    def test_wiki_request_url(self):
        self.assertEqual(self.requestor.url, config.WIKIPEDIA_URL)

    @mock.patch('requests.get')
    def test_wiki_request_for_page_id_ok(self, mocked_requests_get):

        expected_result = {
            "batchcomplete": "",
            "continue": {
                "sroffset": 1,
                "continue": "-||extracts"
            },
            "query": {
                "searchinfo": {
                    "totalhits": 3882
                },
                "search": [
                    {
                        "ns": 0,
                        "title": "Tour Eiffel",
                        "pageid": 1359783,
                        "size": 129846,
                        "wordcount": 14637,
                        "snippet": 'Pour les articles homonymes, voir <span class="searchmatch">Tour</span> <span class="searchmatch">Eiffel</span> (homonymie). L\'introduction de cet article est soit absente, soit non conforme aux conventions de Wikipédia',
                        "timestamp": "2020-03-10T03:15:13Z"
                    }
                ]
            }
        }

        mocked_response = self._setup_mocked_response(expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.url_ask)

        self.assertDictEqual(response, expected_result["query"])

    @mock.patch('requests.get')
    def test_wiki_request_for_extract_ok(self, mocked_requests_get):

        expected_result = {
            "batchcomplete": "",
            "query": {
                "pages": {
                    1359783: {
                        "pageid": 1359783,
                        "ns": 0,
                        "title": "Tour Eiffel",
                        "extract": "La tour Eiffel est une tour de fer puddlé de 324 mètres de hauteur (avec antennes) "
                                   "située à Paris, à l’extrémité nord-ouest du parc du Champ-de-Mars en bordure de la "
                                   "Seine dans le 7e arrondissement."
                                   " Son adresse officielle est 5, avenue Anatole-France."
                    }
                }
            }
        }

        mocked_response = self._setup_mocked_response(expected_result)
        mocked_requests_get.return_value = mocked_response
        response, code = self.requestor.wiki_request(self.url_ask)
        mocked_requests_get.assert_called_once_with(self.url_ask)

        self.assertDictEqual(response, expected_result["query"])

    @mock.patch('requests.get')
    def test_wiki_request_raise_for_status(self, mocked_requests_get):

        mocked_response = self._setup_mocked_response({'query': None}, ok=False)
        mocked_requests_get.return_value = mocked_response

        self.requestor.wiki_request(self.url_ask)

        mocked_response.raise_for_status.assert_called_once_with()

    @mock.patch('gpapp.gpmodules.wiki_requestor.WikiRequestor.wiki_request')
    def test_page_id_search_ok(self, mocked_wiki_request):
        expected_search_item = {
            "ns": 0,
            "title": "Tour Eiffel",
            "pageid": 1359783,
            "size": 129846,
            "wordcount": 14637,
            "snippet": (
                'Pour les articles homonymes, voir <span class="searchmatch">Tour</span> '
                '<span class="searchmatch">Eiffel</span> (homonymie). '
                'L\'introduction de cet article est soit absente, soit non conforme aux conventions de Wikipédia'
            ),
            "timestamp": "2020-03-10T03:15:13Z"
        }
        expected_result = {
            "searchinfo": {
                "totalhits": 3882
            },
            "search": [
                expected_search_item
            ]
        }

        expected_code = 200
        mocked_wiki_request.return_value = expected_result, expected_code,
        response, code = self.requestor.page_id_search()
        mocked_wiki_request.assert_called_once_with(
            self.requestor.url + "&list=search&srlimit=1&srsearch=" + self.requestor.key_words
        )

        self.assertDictEqual(response, dict(
            title=expected_search_item['title'],
            page_id=expected_search_item['pageid'],
            mode="exact"
        ))

    @mock.patch('gpapp.gpmodules.wiki_requestor.WikiRequestor.wiki_request')
    def test_page_id_search_error(self, mocked_wiki_request):
        expected_error = 'Network unavailable'
        mocked_wiki_request.side_effect = requests.HTTPError(expected_error)

        with self.assertRaises(requests.HTTPError) as ctx:
            _ = self.requestor.page_id_search()

        self.assertEqual(str(ctx.exception), expected_error)

    @mock.patch('gpapp.gpmodules.wiki_requestor.WikiRequestor.page_id_search')
    @mock.patch('gpapp.gpmodules.wiki_requestor.WikiRequestor.wiki_request')
    def test_extract_ok(self, mocked_page_id_search, mocked_wiki_request):

        expected_code = 200
        id_expected_result = {
            "title": "Tour Eiffel",
            "pageid": 1359783,
            "mode": "exact"
        }
        wiki_expected_result = {
            "query": {
                "pages": {
                    1359783: {
                        "pageid": 1359783,
                        "ns": 0,
                        "title": "Tour Eiffel",
                        "extract": "La tour Eiffel est une tour de fer puddlé de 324 mètres de hauteur (avec antennes) "
                                   "située à Paris, à l’extrémité nord-ouest du parc du Champ-de-Mars en bordure de la "
                                   "Seine dans le 7e arrondissement."
                                   " Son adresse officielle est 5, avenue Anatole-France."
                    }
                }
            }
        }
        id_mocked_response = self._setup_mocked_response(id_expected_result, magic=True)
        mocked_page_id_search.return_value = id_mocked_response, expected_code
        wiki_mocked_response = self._setup_mocked_response(wiki_expected_result, magic=True)
        mocked_wiki_request.return_value = wiki_mocked_response, expected_code
        response, code = self.requestor.extract()
        mocked_page_id_search.assert_called_once_with(self.requestor.url +
                                                      "&exintro=1&explaintext=1&exsentences=2&pageids=" +
                                                      str(id_expected_result['pageid']))

        self.assertDictEqual(response, dict(
            title=id_expected_result['title'],
            page_id=id_expected_result['pageid'],
            mode=id_expected_result['mode'],
            extract=wiki_expected_result['query']['pages'][1359783]['extract']
        ))

    # @mock.patch('gpapp.gpmodules.wiki_requestor.WikiRequestor.page_id_search')
    # def test_extract_ok(self, mocked_page_id_search):
    #
    #     id_expected_result = {
    #         "title": "Tour Eiffel",
    #         "pageid": 1359783,
    #         "mode": "exact"
    #     }
    #
    #     id_mocked_response = self._setup_mocked_response(id_expected_result)
    #     mocked_page_id_search.return_value = id_mocked_response
    #     response, code = self.requestor.extract()
    #     mocked_page_id_search.assert_called_once_with(self.requestor.url +
    #                                                   "&exintro=1&explaintext=1&exsentences=2&pageids=" +
    #                                                   id_expected_result['pageid'])
    #
    #     self.assertDictEqual(response, dict(
    #         title=id_expected_result['title'],
    #         page_id=id_expected_result['pageid'],
    #         mode=id_expected_result['mode'],
    #         extract=wiki_expected_result['query']['pages'][1359783]['extract']
    #     ))

    # @mock.patch('requests.get')
    # def extract_error(self, mocked_requests_get):
    #
    #     mocked_response = self._setup_mocked_response(self.expected_result)
    #     mocked_requests_get.return_value = mocked_response
    #     response, code = self.requestor.extract()
    #     mocked_requests_get.assert_called_once_with(self.requestor.url)
    #
    #     self.assertDictEqual(response, dict(
    #         #title=self.expected_result['query']['pages'][1359783]['title'],
    #         #extract=self.expected_result['query']['pages'][1359783]['extract']
    #     ))
