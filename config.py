#! /usr/bin/env python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

# GOOGLE_JS_KEY = os.environ.get('GOOGLE_JS_KEY')
GOOGLE_MAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
WIKIPEDIA_URL = "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&format=json"
