import json
import os 
import requests

#ok this package sucks dont use 
#import plotly.express as px
import pandas as pd

from secrets import spotify_user_id, spotify_token_1 

class SpotifyAPIs: 

	def __init__(self): 
		self.user_id = spotify_user_id
		self.spotify_token = spotify_token_1
		self.topArtistsIDs = []
		self.topTrackIDs = [] 
		
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
		topTracks = [] 
		for item in response_json['items']: 
			if item['name'] and item['name'] not in topTracks: 
				topTracks.append(item['name'])
				if item['id'] not in self.topTrackIDs: 
					self.topTrackIDs.append(item['id'])
		return topTracks
	
	def analyseTopSongs(self): 
		if len(self.topTrackIDs) == 0: 
			return None 

		averageFeatures = {
			"danceability": 0 , 
			"energy": 0 , 
			"speechiness": 0,
			"liveness": 0,
			"valence": 0,
  			"count": 0
		}

		for trackID in self.topTrackIDs: 
			q = 'https://api.spotify.com/v1/audio-features/{}'.format(trackID)
			r = requests.get(
				q, 
				headers = {
					"Content-Type": "application/json",
					"Authorization": "Bearer {}".format(self.spotify_token),
				}
			)
			response_json = r.json() 
			if response_json["danceability"]: 
				averageFeatures["danceability"] = (averageFeatures["danceability"]*averageFeatures["count"] + response_json["danceability"]) / (averageFeatures["count"] + 1)
			if response_json["energy"]: 
				averageFeatures["energy"] = (averageFeatures["energy"]*averageFeatures["count"] + response_json["energy"]) / (averageFeatures["count"] + 1)
			if response_json["speechiness"]: 
				averageFeatures["speechiness"] = (averageFeatures["speechiness"]*averageFeatures["count"] + response_json["speechiness"]) / (averageFeatures["count"] + 1)
			if response_json["liveness"]: 
				averageFeatures["liveness"] = (averageFeatures["liveness"]*averageFeatures["count"] + response_json["liveness"]) / (averageFeatures["count"] + 1)
			if response_json["valence"]: 
				averageFeatures["valence"] = (averageFeatures["valence"]*averageFeatures["count"] + response_json["valence"]) / (averageFeatures["count"] + 1)
			
			averageFeatures["count"] = averageFeatures["count"] + 1

		#{'danceability': 0.6430400000000003, 'energy': 0.5959800000000002, 'loudness': -8.591560000000003, 'liveness': 0.14148600000000003, 'valence': 0.45702800000000005, 'count': 50}
		return averageFeatures

if __name__ == '__main__':
	cp = SpotifyAPIs() 
	print(cp.topArtists())
	print(cp.topTracks())
	# print(cp.analyseTopSongs())
	averageFeatures = cp.analyseTopSongs() 


	if averageFeatures["count"] != 0: 
		# df = pd.DataFrame(dict(
		# 	r=[averageFeatures['danceability'], averageFeatures['energy'], averageFeatures['liveness'], averageFeatures['valence'], averageFeatures['speechiness']],
		# 	theta=['danceability','energy','liveness',
		# 		'valence', 'speechiness']))
		# fig = px.line_polar(df, r='r', theta='theta', line_close=True)
		# fig.show()