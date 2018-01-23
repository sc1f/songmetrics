import sqlite3, os, pathlib, pickle

class DB:
    # todo: architectural restructuring
    def __init__(self, db_name:str='song_metric'):
        # use working directory for now
        db_path = pathlib.Path(os.getcwd() + '/' + db_name + '.sqlite')
        conn = sqlite3.connect(str(db_path.resolve()))
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS artists '
                  '("id" TEXT NOT NULL UNIQUE, '
                  '"name" TEXT, "tracks" BLOB)')

        # place our audio features into the tracks table
        c.execute('CREATE TABLE IF NOT EXISTS tracks '
                  '(id TEXT NOT NULL UNIQUE, '
                  'name TEXT, '
                  'artist_id TEXT NOT NULL UNIQUE,'
                  'artist_name TEXT,'
                  'album_id TEXT,'
                  'album_name TEXT,'
                  'danceability REAL,'
                  'energy REAL,'
                  'key REAL,'
                  'loudness REAL,'
                  'mode REAL,'
                  'speechiness REAL,'
                  'acousticness REAL,'
                  'instrumentalness REAL,'
                  'liveness REAL,'
                  'valence REAL,'
                  'tempo REAL,'
                  'FOREIGN KEY (artist_id) REFERENCES artists(id))')

        self.db = conn
        self.db_cursor = c
        self.db_path = db_path


    def getTracksByArtistId(self, artist_id: str):
        self.db_cursor.execute('SELECT * FROM artists WHERE id = ?', artist_id)
        rows = self.db_cursor.fetchall()
        return rows

    def processTracksForInsertion(self, tracks: list):
        processed_tracks = []
        for track in tracks:
            processed_track = {
                'id': track['id']
            }
    def setTracksByArtistId(self, artist_meta: dict, tracks: list) -> bool:
        artist_id = artist_meta['id']
        artist_name = artist_meta['name']
        try:
            self.db_cursor.execute('SELECT id from artists WHERE id = ?', artist_id)
            data = self.db_cursor.fetchone()
            if data is None:
                raise LookupError("Artist doesn't currently exist - create the new artist first.")
            # todo: at what point do we take this and just django it?
            self.db_cursor.execute('INSERT INTO tracks '
                                   'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',)
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            print('ERROR: artist ' + artist_name + 'already exists.')
            return False
            # serialize tracks
            # todo: do we actually need pickle? how do we want to play with the data? isn't it faster to have SQL sort our data once it gets there?
            # todo: if so, then focus should be on the db layer, not the api logic - that just fetches, end of story
            #pickled_tracks = pickle.dumps()
            #self.db_cursor.execute('INSERT INTO artists ("id", "name", "tracks") VALUES (?, ?, ?)', [artist_id, artist_name, tracks])
            # 1. check if the artist exists


