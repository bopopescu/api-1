import mysql.connector
import json
import werkzeug

from flask import Flask
from flask import request
from flask import Response
from mysql.connector import Error

app = Flask(__name__, template_folder='templates')


def getConnector():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='api',
                                       user='root',
                                       password='Bananas312%%')
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        return False


@app.route('/')
def index():
    return 'Hello world!'


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400


@app.route('/api/recipes', methods=['GET'])
def getRecipes():
    conn = getConnector()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, name, slug FROM recipes__recipe;"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)
    return Response(json.dumps(
        {
            "code": 200,
            "message": "ok",
            "datas": rows
        }), 200, {
        'Content-Type': 'Application/json'
    	})


if __name__ == '__main__':
    app.run()
    from werkzeug.serving import run_simple

    # application.debug = True
    run_simple('0.0.0.0', 000, application)
