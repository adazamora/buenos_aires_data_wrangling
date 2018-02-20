import sqlite3
import csv

''' This code was obtained from this link 
https://discussions.udacity.com/t/creating-db-file-from-csv-files-with-non-ascii-unicode-characters/174958/7 '''


sqlite_file = 'BuenosAires.db'
#
# # Connect to the database
conn = sqlite3.connect(sqlite_file)
#
# # Get a cursor object
cur = conn.cursor()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
)
''')
# commit the changes
conn.commit()

cur.execute('''
    CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
)
''')
# commit the changes
conn.commit()

cur.execute('''
    CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
)
''')
# commit the changes
conn.commit()

cur.execute('''
    CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
)
''')
# commit the changes
conn.commit()

cur.execute('''
    CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
)
''')
# commit the changes
conn.commit()


def fill_tables(csvfile, tablename, sqlite_file):
    """ Fills a database table

    Args:
        csvfile(str): name of the csv data file
        tablename(str): name of the table
        sqlite_file(str): name of the data base
        """
    conn = sqlite3.connect(sqlite_file)
    cur = conn.cursor()
    with open(csvfile, 'r', encoding="utf8") as f:
        reader = csv.DictReader(f) # comma is default delimiter
        headers_list = reader.fieldnames
        headers_names = ', '.join(headers_list)
        headers_names = '(' + headers_names + ')'
        interrogation_list = ['?'] * len(headers_list)
        interrogation = ', '.join(interrogation_list)
        interrogation = '(' + interrogation + ');'
        to_database = []
        for row_dict in reader:
            list_to_db = []
            for title in headers_list:
                list_to_db.append(row_dict[title])
            to_database.append(list_to_db)
    # insert the formatted data
    cur.executemany("INSERT INTO " + tablename + headers_names + " VALUES " + interrogation, to_database)
    # commit the changes
    conn.commit()
    conn.close()

fill_tables('nodes.csv', 'nodes', 'BuenosAires.db')
fill_tables('nodes_tags.csv', 'nodes_tags', 'BuenosAires.db')
fill_tables('ways.csv', 'ways', 'BuenosAires.db')
fill_tables('ways_tags.csv', 'ways_tags', 'BuenosAires.db')
fill_tables('ways_nodes.csv', 'ways_nodes', 'BuenosAires.db')

conn.close()
