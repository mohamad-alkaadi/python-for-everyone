import sqlite3 as sql
import re
conn = sql.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute(''' 
    CREATE TABLE Counts (org TEXT, count INTEGER)
''')

fname = 'mbox.txt'

fh = open(fname)

for line in fh:
    if not line.startswith('From: '):continue
    match = re.search(r"@([^\n]+)",line)
    if match:
        org = match.group(1)
    else:
        continue
    
    cur.execute('''SELECT count FROM Counts WHERE org = ? ''', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) VALUES (?,1)''',(org,))
    else:
        cur.execute('UPDATE Counts SET count= count + 1 WHERE org = ?', (org,))
    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()

    
