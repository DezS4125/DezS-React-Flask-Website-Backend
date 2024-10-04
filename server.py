from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

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

INSERT_TO_DO_ITEM="""INSERT INTO to_do_items (to_do_content, checked, creation_date)
VALUES  (%s,%s,%s) RETURNING id;"""

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
        data = request.get_json()
        content = data["content"]
        checked = data["checked"]
        creation_date = data["creation_date"]
        conn=None
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TO_DO_ITEM_TABLE)
                cur.execute(INSERT_TO_DO_ITEM,(content,checked,creation_date))
                item_id= cur.fetchone()[0]
                cur.close()
                conn.commit()
                return {"id": item_id, "message": "Item added."}, 201
    except Exception as error:
        print(error)
    finally:
        if conn != None:
            conn.close()

@app.delete("/api/todo")
def deleteItem():
    try:
        data = request.get_json()
        id = data["id"]
        conn=None
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                statement="call delete_to_do_item(%s);"
                cur.execute(statement,(id,))
                cur.close()
                return {"id": id, "message": "Item deleted."}, 202
    except Exception as error:
        print(error)
    finally:
        if conn != None:
            conn.close()



@app.post("/api/test")
def test():
    data=request.get_json()
    content = data["content"]
    checked = data["checked"]
    creation_date = data["creation_date"]
    print(type(content))
    print(type(checked))
    print(type(creation_date))
    # conn=None
    return {"message": "Cooke."}, 201

if __name__ =="__main__":
    app.run(debug=True, port=8080)