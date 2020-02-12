# test_view ?
from gpapp import app


def mock_fonctionamocker():
    # rq : peut etre def dans la fonction de test si n'est pas utilise apres
    return "resultat attendu"


def test_nomfonction_cequejeteste(monkeypatch):
    # soit ...(contexte de test)
    monkeypatch.setattr("gpapp.app.fonctionamocker", mock_fonctionamocker())
    # quand... (action)
    result = app.nomfonction()
    # alors je constate que... (resultat)
    assert result == "resultat attendu"
