import json
import os 
import requests

from secrets import spotify_user_id, spotify_token_1 

class SpotifyAPIs: 

	def __init__(self): 
		self.user_id = spotify_user_id
		self.spotify_token = spotify_token_1
		
	def topArtists(self): 
		q = "https://api.spotify.com/v1/me/top/{}?time_range={}&limit={}".format("artists", "long_term", "50")
		r = requests.get(
			q, 
			headers = {
				"Content-Type": "application/json",
				"Authorization": "Bearer {}".format(self.spotify_token),
			}
		)
		response_json = r.json() 
		topArtists = [] 
		for item in response_json['items']: 
			if item['name']: 
				topArtists.append(item['name'])
		return topArtists

	def topTracks(self): 
		q = "https://api.spotify.com/v1/me/top/{}?time_range={}&limit={}".format("tracks", "long_term", "50")
		r = requests.get(
			q, 
			headers = {
				"Content-Type": "application/json",
				"Authorization": "Bearer {}".format(self.spotify_token),
			}
		)
		response_json = r.json() 
		topArtists = [] 
		for item in response_json['items']: 
			if item['name']: 
				topArtists.append(item['name'])
		return topArtists

if __name__ == '__main__':
	cp = SpotifyAPIs() 
	print(cp.topArtists())
	print(cp.topTracks())