#! /usr/bin/env python

from gpapp.gpmodules import parser, map_requestor, wiki_requestor

# modele
def mock_fonctionamocker():
    # rq : peut etre def dans la fonction de test si n'est pas utilise apres
    return "resultat attendu"


def test_nomfonction_cequejeteste(monkeypatch):
    # soit ...(contexte de test (setup))
    monkeypatch.setattr("gpapp.app.fonctionamocker", mock_fonctionamocker())
    # quand... (action)
    result = parser.nomfonction()
    # alors je constate que... (resultat)
    assert result == "resultat attendu"
# fin modele


class ParserTest:
    """Class for tests of functions contained in module parser.py"""
    def test_parsing_(self):
        # soit ...(contexte de test (setup))
        question = ""
        # quand... (action)
        result = parser.get_key_words(question)
        # alors je constate que... (resultat)
        assert result == "resultat attendu"


class MapTest:
    """Class for tests of functions contained in module map_requestor.py"""


class WikiTest:
    """Class for tests of functions contained in module wiki_requestor.py"""
