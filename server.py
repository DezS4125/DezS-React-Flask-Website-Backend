from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import json
import datetime

app= Flask(__name__)
cors = CORS(app, origin="*")

query_to_do_items="select * from to_do_items"

CREATE_TO_DO_ITEM_TABLE="""create table if not exists to_do_items(
	id serial primary key,
	to_do_content text not null default '',
	checked boolean default false,
	to_do_item_date timestamp default null,
	creation_date date default current_date
);"""

INSERT_TEST_TO_DO_ITEM="""INSERT INTO to_do_items (to_do_content, checked, to_do_item_date, creation_date)
VALUES
  ('Buy groceries', false, '2024-10-01 15:00:00', '2024-09-24'),
  ('Finish homework', true, '2024-09-25 18:00:00', '2024-09-24'),
  ('Meet with client', false, '2024-09-26 10:30:00', '2024-09-24'),
  ('Clean the house', false, null, '2024-09-24'),
  ('Go for a run', true, '2024-09-23 07:00:00', '2024-09-24');"""

CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)


CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)

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
def queryToDoItems():
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

@app.post("/api/todo")
def addItem():
    try:
        conn=None
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TO_DO_ITEM_TABLE)
                cur.execute(INSERT_TEST_TO_DO_ITEM)
                cur.close()
                conn.commit()
                return {"message": "Item added."}, 201
    except Exception as error:
        print(error)
    finally:
        if conn != None:
            print("Connection failed")
            conn.close()

@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room"]
    try:
        date = datetime.datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.datetime.now()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id, temperature, date))
    return {"message": "Temperature added."}, 201


if __name__ =="__main__":
    app.run(debug=True, port=8080)