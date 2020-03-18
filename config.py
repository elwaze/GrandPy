#! /usr/bin/env python
import os

GOOGLE_MAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY', "AIzaSyBmyCPrDf0hIaBEaHYvIIVfGj_tBwLCWsU")
WIKIPEDIA_URL = "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&format=json"
