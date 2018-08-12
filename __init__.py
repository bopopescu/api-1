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

@app.errorhandler(400)
def error400(error):
    return json.dumps({"code" : 400, "message" : "Bad Request"}), 400
@app.errorhandler(401)
def error401(error):
    return json.dumps({"code" : 401, "message" : "Unauthorized"}), 401
@app.errorhandler(403)
def error403(error):
    return json.dumps({"code" : 403, "message" : "Forbidden"}), 403
@app.errorhandler(404)
def error404(error):
    return json.dumps({"code" : 404, "message" : "Not Found"}), 404

@app.route('/')
def index():
    return json.dumps({"API RTP Sarah Al Janabi" : "Etape 1"})


@app.route('/api/recipes.json', methods=['GET'])
def getRecipes():
    conn = getConnector()
    if not conn:
        return Response(json.dumps(
            {
                "code":200,
                "message" : "no connector"
            }), 200, {
            'Content-Type': 'Application/json'
        })
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
