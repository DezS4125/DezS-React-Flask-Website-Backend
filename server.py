from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
import json

app= Flask(__name__)
# cors = CORS(app, origin="http://localhost:5173")
cors = CORS(app, origin="*")

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='mywebsite',
                            user=os.environ['WEBSITE_DB_USERNAME'],
                            password=os.environ['WEBSITE_DB_PASSWORD'])
    return conn


@app.route("/api/todo", methods=['GET'])
def members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select * from to_do_items")
    to_do_items = cur.fetchall()
    cur.close()
    conn.close()
    return to_do_items

if __name__ =="__main__":
    app.run(debug=True, port=8080)