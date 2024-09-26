from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import json

app= Flask(__name__)
cors = CORS(app, origin="*")

query_to_do_items="select * from to_do_items"

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='mywebsite',
                            user=os.environ['WEBSITE_DB_USERNAME'],
                            password=os.environ['WEBSITE_DB_PASSWORD'])
    return conn

def convert_to_json(data):
    if isinstance(data[0], psycopg2.extras.DictRow):
        data = [dict(row) for row in data]
    json_data = json.dumps(data, default=str)
    return json_data

@app.get("/api/todo")
def queryToDo():
    try:
        conn=None
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query_to_do_items)
                to_do_items = cur.fetchall()
                cur.close()
                return convert_to_json(to_do_items),200
    except Exception as error:
        print(error)
    finally:
        if conn != None:
            conn.close()




if __name__ =="__main__":
    app.run(debug=True, port=8080)