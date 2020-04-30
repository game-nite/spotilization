import json
import os 
import requests

from secrets import spotify_user_id, spotify_token_1 

class SpotifyAPIs: 

	def __init__(self): 
		self.user_id = spotify_user_id
    	self.spotify_token = spotify_token_1
	
	# def topArtists(self): 
