from app import app, developer_key, youtube
import pprint
import requests
from flask import jsonify, render_template


def get_channel_ID(channel_name):
	url = "https://www.googleapis.com/youtube/v3/channels?key={}&forUsername={}&part=id".format(developer_key,
																								channel_name)

	print("Channel Name: ", channel_name)
	response = requests.get(url)

	data = response.json()
	print("DATA: ")
	pprint.pprint(data)

	if len(data['items']) > 0:
		return data['items'][0]['id']

	else:
		return -1


@app.route('/index')
def index():
	return "Oh, Hello There!"


@app.route('/playlist/<channel_name>', methods=['GET'])
def playlist(channel_name):

	channel_id = get_channel_ID(channel_name)

	if channel_id != -1:

		request = youtube.playlists().list(
			part="snippet,contentDetails",
			channelId=channel_id,
			maxResults=25
		)

		response = request.execute()

		pprint.pprint(response['items'])

		return render_template('playlist.html', playlists=response['items'])

	else:
		return "Invalid Channel"


@app.route('/videos/<pid>')
def videos(pid):

	request = youtube.playlistItems().list(
		part="snippet,contentDetails",
		maxResults=25,
		playlistId=pid
	)

	response = request.execute()

	pprint.pprint(response['items'])

	return render_template('index.html', videos=response['items'], pid = pid)


@app.route('/play/<pid>/<vid>')
def play(vid, pid):

	request = youtube.playlistItems().list(
		part="snippet,contentDetails",
		maxResults=25,
		playlistId=pid,
		videoId=vid
	)
	response = request.execute()

	return render_template('play.html', video=response['items'])
