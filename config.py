#! /usr/bin/env python
import os

APP_ROOTDIR = os.path.dirname(__file__)

SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_MAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY', '')
WIKIPEDIA_URL = "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&format=json"
WIKILINK = "https://fr.wikipedia.org/wiki/"
GOOGLE_MAPS_LINK = f"https://maps.googleapis.com/maps/api/js?key={GOOGLE_KEY}&callback=initMap"

STOP_WORDS_FILENAME = os.path.join(APP_ROOTDIR, 'gpapp', 'gpmodules', 'stop_words.json')
