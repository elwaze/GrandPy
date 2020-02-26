#! /usr/bin/env python

import json
import urllib.request
from io import BytesIO
from gpapp.gpmodules.parser import Parser
from gpapp.gpmodules.map_requestor import MapRequestor
# from gpapp.gpmodules.wiki_requestor import WikiRequestor

# # modele
# def mock_fonctionamocker():
#     # rq : peut etre def dans la fonction de test si n'est pas utilise apres
#     return "resultat attendu"
#
#
# def test_nomfonction_cequejeteste(monkeypatch):
#     # soit ...(contexte de test (setup))
#     monkeypatch.setattr("gpapp.app.fonctionamocker", mock_fonctionamocker())
#     # quand... (action)
#     result = parser.nomfonction()
#     # alors je constate que... (resultat)
#     assert result == "resultat attendu"
# # fin modele


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


class MapTest:
    """Class for tests of functions contained in module map_requestor.py"""
    def setup(self):
        """Setup for the google maps requestor tests"""
        self.requestor = MapRequestor("tour+eiffel")

    def test_api_request_ok(self, monkeypatch):
        results = {

        }
        self.results = BytesIO(json.dumps(results).encode())

        def mockreturn(request):
            return self.results

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)
        # expected result
        assert self.requestor.gmap_address(self.requestor.query_keywords) is True
        assert self.requestor.latitude == 20
        assert self.requestor.longitude == 30

    def test_api_request_empty(self):
        pass

    def test_api_request_notfound(self):
        pass


class WikiTest:
    """Class for tests of functions contained in module wiki_requestor.py"""
