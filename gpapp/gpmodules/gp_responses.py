#! /usr/bin/env python
""" Module generating the GrandPy responses sent to the user."""


class ResponseGenerator:
    """Class which returns the formatted response."""

    def __init__(self):
        # wrong question
        self.wrong_question = "Je n'ai pas bien compris mon petit, tu peux reformuler ta demande ?"
        self.place_found = "Tadaaaaa! voilà ce que tu cherches : "
        self.place_not_found = "Je n'ai pas trouvé ce que tu cherches. Peux-tu préciser ta recherche ?"
        self.wiki_ok = "Ah, que de souvenirs me reviennent ! Savais-tu que "
        # self.wiki_exact = "Mais je connais bien ce lieu ! Savais-tu que "
        # self.wiki_nearby = "Tiens, ça me fait penser que pas loin de là, il y a "
        self.wiki_not_found = "Ben voilà, c'est là, par contre, j'ai beau savoir des tas de choses, " \
                              "je ne connais rien d'intéressant à proximité !"
