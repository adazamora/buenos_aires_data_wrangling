import sqlite3

sqlite_file = 'BuenosAires.db'    # name of the sqlite database file
#
# # Connect to the database
conn = sqlite3.connect(sqlite_file)
#
# # Get a cursor object
cur = conn.cursor()

print('Top 10 users contributors')

cur.execute("""SELECT nodes.user, count(*) as num FROM nodes, ways, ways_nodes
            WHERE nodes.id = ways_nodes.node_id AND ways_nodes.id = ways.id
            GROUP BY nodes.uid, ways.uid ORDER BY num desc LIMIT 10""")
print(cur.fetchall())

print('\n' 'Grouping nodes by timestamp to know the time of the first and last modification')

cur.execute('SELECT max(timestamp) as max, min(timestamp) as min FROM nodes')
print(cur.fetchall())

print('\n' 'Grouping ways by timestamp to know the time of the first and last modification')

cur.execute('SELECT max(timestamp) as max, min(timestamp) as min FROM ways')
print(cur.fetchall())

print('\n' 'Top 10 amenities')

cur.execute("""SELECT value, count(*) as num from nodes_tags where key = 'amenity' GROUP BY value ORDER BY num desc
            LIMIT 10""")
print(cur.fetchall())

print('\n'  'The name and number of the most popular ice-cream shops in Buenos Aires')

cur.execute("""SELECT b.value, count(*) as num
            FROM nodes_tags as a, nodes_tags as b
            WHERE a.id = b.id AND a.key = 'amenity' AND a.value = 'ice_cream' AND b.key = 'name'
            GROUP BY b.value ORDER BY num desc LIMIT 5""")
print(cur.fetchall())

print('\n' 'The most common fast food restaurants')

cur.execute("""SELECT b.value, count(*) as num
            FROM nodes_tags as a, nodes_tags as b
            WHERE a.id = b.id AND a.key = 'amenity' AND a.value = 'fast_food' AND b.key = 'name'
            GROUP BY b.value ORDER BY num desc LIMIT 5""")
print(cur.fetchall())

print('\n' 'The most common cuisine type restaurants')

cur.execute("""SELECT b.value, count(*) as num
            FROM nodes_tags as a, nodes_tags as b
            WHERE a.id = b.id AND a.key = 'amenity' AND a.value = 'restaurant' AND b.key = 'cuisine'
            GROUP BY b.value ORDER BY num desc LIMIT 5""")
print(cur.fetchall())

print('\n' 'Types of ways surfaces')

cur.execute("""SELECT value, count(*)*100.0 /
            (SELECT count(*) FROM ways_tags WHERE key = 'surface') as percentage
            FROM ways_tags GROUP BY value HAVING key = 'surface'
            ORDER BY percentage desc LIMIT 10""")
print(cur.fetchall())

print('\n' 'The name of the highways with the most number of lanes')

cur.execute("""SELECT a.value, b.value
            FROM ways_tags as a, ways_tags as b
            WHERE a.id = b.id AND a.key = 'name' AND b.key = 'lanes' AND CAST(b.value AS INTEGER) > 7
            GROUP BY a.value ORDER BY CAST(b.value AS INTEGER) asc, CAST(a.value AS INTEGER) asc""")
print(cur.fetchall())
