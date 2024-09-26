import psycopg2
import psycopg2.extras
import os


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='mywebsite',
                            user=os.environ['WEBSITE_DB_USERNAME'],
                            password=os.environ['WEBSITE_DB_PASSWORD'])
    return conn

conn = get_db_connection()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("select * from to_do_items")
to_do_items = cur.fetchall()
cur.close()
conn.close()
print(dict(to_do_items[0])) 
