import spotipy, bisect
from spotipy.oauth2 import SpotifyClientCredentials

# TODO: object oriented implementation

class Tracks:
    # todo: object-oriented, a new Tracks instance for each new search/artist?
    def __init__(self):
        pass

def init(client_id, client_secret):
    # provides a single instance of spotipy for us to use across functions
    if client_id is None:
        raise KeyError("Spotify client ID was not provided!")
    cred_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_interface = spotipy.Spotify(client_credentials_manager=cred_manager)
    return spotipy_interface

'''
def get_all_tracks_by_album(sp, query):
    search = sp.search(q=query, limit=1, type='album')['tracks']['items'][0]
    album_id = search['album']['id']
    return sp.album_tracks(album_id=album_id)['items']
'''

def get_all_tracks_by_artist(sp, query):
    # todo: optimize, how do we return the necessary data?
    artist_tracks = []
    search = sp.search(q=query, limit=1)['tracks']['items'][0]
    artist = search['artists'][0]

    if artist['name'].lower() != query.lower():
        raise KeyError("Artist name does not match queried name.")

    artist_albums = sp.artist_albums(artist_id=artist['id'], album_type='album')[
        'items']  # we analyse only albums, no compilations/appearances

    for album in artist_albums:
        if len(album['artists']) > 1:
            # skip anything with multiple artists - Planetarium, etc.
            continue
        tracks = sp.album_tracks(album_id=album['id'])['items']
        for track in tracks:
            artist_tracks.append(track)

    return artist['id'], artist['name'], artist_tracks

def get_audio_features(sp, tracks):
    features = []
    print(tracks)
    for t in tracks:
        id = t['id']
        name = t['name']
        audio_feature = sp.audio_features(id)[0]
        audio_feature['name'] = name
        features.append(audio_feature)
    return features

def sort_tracks_by_audio_feature(sp, feature, tracks):
    track_features = []
    valid_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo']
    if feature not in valid_features:
        raise IndexError("You didn't query a valid feature!")
    # pluck specified feature and sort in one pass
    for track in tracks:
        meta = {
            'selected_feature': feature,
            'feature_value': track[feature],
            'name': track['name']
        }
        track_features.append(meta)
    track_features.sort(key=lambda t: t['feature_value'])
    return track_features

