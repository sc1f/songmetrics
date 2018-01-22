import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def init_spotipy(client_id, client_secret):
    # provides a single instance of spotipy for us to use across functions
    if client_id is None:
        raise KeyError("Spotify client ID was not provided!")
    cred_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_interface = spotipy.Spotify(client_credentials_manager=cred_manager)
    return spotipy_interface

def get_all_tracks_by_artist(sp, query):
    all_tracks = []
    search = sp.search(q=query, limit=1)['tracks']['items'][0]
    artist = search['artists'][0]

    if artist['name'].lower() != query.lower():
        raise KeyError("Artist name does not match queried name.")

    artist_albums = sp.artist_albums(artist_id=artist['id'], album_type='album')['items'] # we analyse only albums, no compilations/appearances

    for album in artist_albums:
        if len(album['artists']) > 1:
            # skip anything with multiple artists - Planetarium, etc.
            continue
        tracks = sp.album_tracks(album_id=album['id'])['items']
        for track in tracks:
            all_tracks.append(track)

    return all_tracks

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