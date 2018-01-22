import os, pathlib
import get_tracks

# read .env
dotenv = pathlib.Path(os.getcwd() + '/.env')
if dotenv.is_file():
    with dotenv.open(mode='r') as env:
        envvars = env.readlines()
        for line in envvars:
            key, value = [l.strip('\n') for l in line.split('=')]
            if len(key) > 0 and len(value) > 0:
                os.environ[key] = value
                print(key, "has been set.")
            else:
                raise KeyError("There is a problem with your .env file! Make sure all credentials are set properly.")

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
GENIUS_API_KEY = os.environ['GENIUS_API_KEY']

# spawn exactly one spotipy instance
sp = get_tracks.init_spotipy(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
# start grabbing tracks and features
sufjan_tracks = get_tracks.get_all_tracks_by_artist(sp, query='sufjan stevens')
sufjan_features = get_tracks.get_audio_features(sp, sufjan_tracks)
print(sufjan_features)

# todo: DB interface so we don't have to get this data and spawn it every time