#! /usr/bin/env python

from gpapp.gpmodules.parser import Parser
# from gpapp.gpmodules.map_requestor import Requestor
# from gpapp.gpmodules.wiki_requestor import Requestor

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
             ["donner", "adresse", "tour", "eiffel"],
             "tour eiffel"),
            ("Salut pépé ! Où je peux trouver le parc de la tête d'or à Lyon ?",
             ["salut", "pépé", "où", "je", "peux", "trouver", "le", "parc", "de", "la", "tête", "d", "or", "à", "Lyon"],
             ["trouver", "parc", "tête", "or", "lyon"],
             "parc tete or lyon")
        ]

    def test_split_question(self):
        """Checks that the split function returns a list of words"""

        # calling function
        for question in self.questions:
            result = self.parser.split(question[0])
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


class WikiTest:
    """Class for tests of functions contained in module wiki_requestor.py"""
