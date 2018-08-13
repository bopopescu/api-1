import mysql.connector
import json
import werkzeug

from flask import Flask
from flask import request
from flask import Response
from mysql.connector import Error
from phpserialize import *
from collections import OrderedDict

app = Flask(__name__)

def getConnector():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='api',
                                       user='root',
                                       password='')
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

def jsonResponse(data = {}, message = '', status = 200):
    return Response(json.dumps(
             {
                "code": status,
                "message": message,
                "datas": data
              }), status, {
              'Content-Type': 'Application/json'
        })


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


#@app.route('/api/recipes/<slug>.json', methods=['GET'])
#def getRecipeBySlug(slug):
#    conn = getConnector()
#    if not conn:
#        return Response(json.dumps(
#            {
#                "code":200,
#                "message" : "no connector"
#            }), 200, {
#            'Content-Type': 'Application/json'
#        })

#    cursor = conn.cursor(dictionary=True)
    #query = "SELECT recipe.id as recipe_id, recipe.slug as slug, recipe.name as recipe_name, user.username, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
#    query = "SELECT recipe.id as recipe_id, recipe.name as recipe_name, recipe.slug as slug, user.username, user.last_login as last_login, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
#    cursor.execute(query, (slug,))
#    rows = cursor.fetchone()

#    if rows is None:
#        return jsonResponse({},'ko', 404)

#    data = {};
#    data['id'] = rows['recipe_id']
#    data['name'] = rows['recipe_name']
#    data['slug'] = rows['slug']
#    data['user'] = {}
#    data['user']['username'] = rows['username']
#    data['user']['id'] = rows['user_id']
#    data['user']['last_login'] = rows['last_login'].strftime("%Y-%m-%d %H:%M:%S")

#    return Response(json.dumps(
#             {
#                "code": 200,
#                "message": "ok",
#                "datas": data
#              }), 200, {
#              'Content-Type': 'Application/json'
#        })


#@app.route('/api/recipes/<slug>/steps.json', methods=['GET'])
#def getStepsForRecipe(slug):
#    conn = getConnector()
#    if not conn:
#        return Response(json.dumps(
#            {
#                "code":200,
#                "message" : "no connector"
#            }), 200, {
#            'Content-Type': 'Application/json'
#        })

#    cursor = conn.cursor(dictionary=True)
#    query = "SELECT step FROM recipes__recipe WHERE slug = %s LIMIT 1;"
#    cursor.execute(query, (slug,))
#    row = cursor.fetchone()
#
#    if row is None:
#        return jsonResponse({},'ko', 404)

#    steps_load = loads(row['step'].encode(), array_hook=OrderedDict)
#    res = []

#    for index in steps_load:
#        res.append(steps_load[index].decode('utf-8'))

#    responseFinal =json.dumps({
#        'code' : 200,
#        'message' : 'ok',
#        'datas' : res
#    })

#    return Response(responseFinal, 200, {'Content-Type': 'Application/json'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
