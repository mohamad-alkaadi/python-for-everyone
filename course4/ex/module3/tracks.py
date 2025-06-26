import sqlite3

conn = sqlite3.connect('trackdb.sqlite')

cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE Album (
    id INTEGER PRIMARY KEY,
    artist_id INTEGER,
    title TEXT UNIQUE
);
CREATE TABLE Track (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    album_id INTEGER,
    len INTEGER,
    rating INTEGER,
    count INTEGER,
);
''')

handle = open('tracks.csv')

for line in handle:
    line = line.strap()
    pieces = line.split(',')
    if len(pieces) < 6: continue
    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    count = pieces[3]
    rating = pieces[4]
    length = pieces[5]

    cur.execute('''
    INSERT IGNORE INTO Artist (name) VALUES ( ? )''',(artist, ))

    cur.excute('SELECT id FROM Artist WHERE name = ? ',(artist, ))
    artist_id = cur.fetchone()[0]

    cur.excute(''' INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)''', (album, artist_id))

    cur.excute('SELECT id FROM Album WHERE title = ?', (album, ))
    album_id = cur.fetchone()[0]

    cur.excute('''INSERT OR REPLACE INITO TRACK (title, album_id, len, rating, count) VALUES ( ?, ?, ?, ?, ?)''',
               (name, album_id, length, rating, count ))
    
    conn.commit()


