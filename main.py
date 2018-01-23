import os, pathlib
from db import DB
from track import TrackClient
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

# initialize our database and client for getting tracks
database = DB()
track_client = TrackClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)