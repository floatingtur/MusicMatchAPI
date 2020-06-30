import json, requests, pprint

# reference for how to format requests
# base url  + the get + the format + rest of get + apikey
# exampleurl = 'http://api.musixmatch.com/ws/1.1/chart.artists.get?format=json&callback=callback&page=1&page_size=3&country=it&apikey=29a80af52fe8077a7979dd5658fbb274'
baseurl = 'http://api.musixmatch.com/ws/1.1/'

apikey = '&apikey=29a80af52fe8077a7979dd5658fbb274'

jsonFormat = '?format=json&callback=callback'


def gettoptenResponse():
    # combine elements to make a request url for top ten songs in the united states
    url = baseurl + 'chart.tracks.get' + jsonFormat + '&page=1&page_10&country=us' + '&f_has_lyrics=1' + apikey

    # loads the results into a json variable called jsonData
    response = requests.get(url)
    jsonData = json.loads(response.text)

    # Loop that fills dictionaries with the names of the songs and their track id
    i = 0

    nameandid = {}

    while i <= len(jsonData['message']['body']['track_list']) - 1:
        nameandid[str(jsonData['message']['body']['track_list'][i]['track']['track_name'])] = str(
            jsonData['message']['body']['track_list'][i]['track']['track_id'])
        i = i + 1

    return nameandid


def gettopArtist():
    # request to musicmatch api for top ten artists
    url = baseurl + 'chart.artists.get' + jsonFormat + '&page=1&page_size=10&country=us' + apikey
    response = requests.get(url)
    jsonData = json.loads(response.text)

    # fills a dictionary with the artist name is key for the artist id
    artistandID = {}

    i = 0

    while i <= len(jsonData['message']['body']['artist_list']) - 1:
        artistandID[jsonData['message']['body']['artist_list'][i]['artist']['artist_name']] = \
        jsonData['message']['body']['artist_list'][i]['artist']['artist_id']
        i = i + 1

    # returns dictionary of artist names and ids
    return artistandID


def getArtistAlbum(artistid):
    # gets the albums for an artist based on who the user choose
    url = baseurl + 'artist.albums.get' + jsonFormat + '&artist_id=' + artistid + '&page=1&page_size=10' + apikey
    response = requests.get(url)
    jsonData = json.loads(response.text)

    # makes a dictionary of the album names and their ids
    albumnameandid = {}

    i =0

    while i <= len(jsonData['message']['body']['album_list']) -1 :
        albumnameandid[jsonData['message']['body']['album_list'][i]['album']['album_name']] = jsonData['message']['body']['album_list'][i]['album']['album_id']
        i = i +1

    #returns the list of album name and ids
    return albumnameandid

def getAlbumTracks(albumId):
    # gets the tracks from an input album id
    url = baseurl + 'album.tracks.get' + jsonFormat + '&album_id=' + albumId + '&page=1&page_size=10&f_has_lyrics=1' + apikey
    response = requests.get(url)
    jsonData = json.loads(response.text)

    # makes a list of the track names and ids
    songNameandID = {}

    i=0

    while i <= len(jsonData['message']['body']['track_list']) - 1:
        songNameandID[jsonData['message']['body']['track_list'][i]['track']['track_name']] = jsonData['message']['body']['track_list'][i]['track']['track_id']
        i = i +1

    # returns list of tracks and ids
    return songNameandID

def getLyrics(trackList):
    global jsonlyricData
    global lyricList

    # Takes a dictionary of track names and ids. Takes the id of each track and replaces it with the lyrics of the track
    for x in trackList:
        lyricUrl = baseurl + 'track.lyrics.get' + jsonFormat + '&track_id=' + str(trackList[x]) + apikey
        response = requests.get(lyricUrl)
        jsonlyricData = json.loads(response.text)

        trackList[x] = jsonlyricData['message']['body']['lyrics']['lyrics_body']

    # returns new dictionary with track names and their lyrics
    return trackList
