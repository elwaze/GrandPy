#! /usr/bin/env python

from flask import Flask, render_template, request, make_response
import json
from gpapp.gpmodules import parser, wiki_requestor, map_requestor, gp_responses
import config


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/api/')
def api():
    question = request.args.get('question')
    response = json.dumps(get_response(question))
    return make_response(response)


parser_ = parser.Parser()


def get_response(question):
    """
    Runs the different modules
    :param question: user's question.
    :return: response to send back to the client
    """

    responses = gp_responses.ResponseGenerator()
    response = {}

    # parser
    parsed_question = parser_.get_keywords(question)

    if parsed_question == "":
        response["gp_response"] = responses.wrong_question
    else:
        # map request
        map_request = map_requestor.MapRequestor(parsed_question)
        searched_place, code = map_request.google_request()
        if code == 200:
            if searched_place['status'] == "OK":
                response['gp_response'] = f"{responses.place_found}" \
                                          f"{searched_place['address']}"
                geometry = f"{searched_place['latitude']}|" \
                           f"{searched_place['longitude']}"
                response['gmap_coord'] = {'lat': searched_place['latitude'],
                                          'lng': searched_place['longitude']}
                # wiki request
                wiki_request = wiki_requestor.WikiRequestor(geometry)
                wiki_result, code = wiki_request.extract()
                if code == 200:
                    title = wiki_result['title'].replace(' ', '_')
                    response["wiki_link"] = f"{config.WIKILINK}{title}"
                    response["wiki_response"] = f"{responses.wiki_ok}"
                    response["wiki_extract"] = wiki_result['extract']
                else:
                    response["wiki_response"] = responses.wiki_not_found
            else:
                response["gp_response"] = responses.place_not_found
        else:
            response["gp_response"] = responses.place_not_found

    return response


if __name__ == "__main__":
    app.run()
