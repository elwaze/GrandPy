#! /usr/bin/env python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

# GOOGLE_JS_KEY = os.environ.get('GOOGLE_JS_KEY')
GOOGLE_MAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
WIKIPEDIA_URL = "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&format=json"
WIKILINK = "https://fr.wikipedia.org/wiki/"
GOOGLE_MAPS_LINK = "https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_KEY + "&callback=initMap"