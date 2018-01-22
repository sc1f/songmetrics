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
        c.execute('CREATE TABLE IF NOT EXISTS tracks '
                  '("id" TEXT NOT NULL UNIQUE, '
                  '"name" TEXT, '
                  'artist_id TEXT NOT NULL UNIQUE, '
                  'FOREIGN KEY (artist_id) REFERENCES artists(id))')

        self.db = conn
        self.db_cursor = c
        self.db_path = db_path


    def get_tracks_by_artist_id(self, artist_id):
        self.db_cursor.execute('SELECT * FROM artists WHERE id = ?', artist_id)
        rows = self.db_cursor.fetchall()
        return rows

    def set_tracks_for_artist_id(self, artist_id, artist_name, tracks):
        # TODO: use tracks table
        print([artist_id, artist_name, tracks])
        try:
            # serialize tracks
            # todo: do we actually need pickle? how do we want to play with the data? isn't it faster to have SQL sort our data once it gets there?
            # todo: if so, then focus should be on the db layer, not the api logic - that just fetches, end of story
            #pickled_tracks = pickle.dumps()
            self.db_cursor.execute('INSERT INTO artists ("id", "name", "tracks") VALUES (?, ?, ?)', [artist_id, artist_name, tracks])
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            print('ERROR: artist ' + artist_name + 'already exists.')
            return False

