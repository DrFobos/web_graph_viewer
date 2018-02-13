import sqlite3
import json
import os
from datetime import datetime as dt

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(APP_ROOT, 'static/myapp.db')


def init_db():
    db = connect_db()
    with open('static/db.sql', 'r') as f:
        sql = f.read()

    db.cursor().execute(sql)
    nodes = [1, 2, 3, 4, 5, 9, 11]
    edges = [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5], [1, 9], [9, 11]]
    date = dt.now().strftime("%Y-%m-%d %X")
    content = json.dumps({'nodes': nodes, 'edges': edges})
    name = 'Example.xls'
    query = "insert into data (name, load_date, content) values (?, ?, ?)"
    db.execute(query, (name, date, content))
    db.commit()
    db.close()


def connect_db():
    return sqlite3.connect(DATABASE)


def write2db(file, nodes, edges):
    date = dt.now().strftime("%Y-%m-%d %X")
    _, name = os.path.split(file.filename)
    content = json.dumps({'nodes': nodes, 'edges': edges})
    db = connect_db()
    query = "insert into data (name, load_date, content) values (?, ?, ?)"
    id_query = "SELECT last_insert_rowid()"
    db.execute(query, (name, date, content))
    last_id = db.execute(id_query).fetchone()[0]
    db.commit()
    db.close()
    return last_id


def read_from_db(id_asked=None):
    db = connect_db()

    if not id_asked:
        query = "select * from data"
        result = db.execute(query)
    else:
        query = "select * from data where id = ?"
        result = db.execute(query, [id_asked])

    entries = [{'id': int(row[0]), 'name': row[1], 'load_date': row[2], 'content': json.loads(row[3])}
               for row in result.fetchall()]
    db.close()
    return entries


if __name__ == '__main__':
    init_db()
