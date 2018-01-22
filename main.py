import os, pathlib
from db import DB
import tracks, lyrics, db, analysis

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

database = DB()
sp = tracks.init(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sufjan_id, sufjan_name, sufjan_tracks = tracks.get_all_tracks_by_artist(sp, query='sufjan stevens')
database.set_tracks_for_artist_id(sufjan_id, sufjan_name, sufjan_tracks)
print(database.get_tracks_by_artist_id(sufjan_id))