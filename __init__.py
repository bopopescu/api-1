import mysql.connector
import json
import werkzeug
import random
import string

from flask import Flask
from flask import request
from flask import Response
from mysql.connector import Error
from phpserialize import *
from collections import OrderedDict
from slugify import slugify

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
def error400():
    return Response(json.dumps(
        {"code": 400,
         "message": "Bad Request"}
    ), 401, {'Content-Type': 'Application/json'})

@app.errorhandler(401)
def error401():
    return Response(json.dumps(
        {"code": 401,
         "message": "Unauthorized"}
    ), 401, {'Content-Type': 'Application/json'})

@app.errorhandler(403)
def error403():
    return Response(json.dumps(
        {"code" : 403,
         "message" : "Forbidden"}
    ), 403, {'Content-Type': 'Application/json'})

@app.errorhandler(404)
def error404(arg):
    return Response(json.dumps(
                {"code" : 404,
                "message" : "Not Found"}
        ), 404, {'Content-Type': 'Application/json'})

def jsonResponse(data = {}, message = '', status = 200):
    return Response(json.dumps(
             {
                "code": status,
                "message": message,
                "datas": data
              }), status, {
              'Content-Type': 'Application/json'})

@app.route('/')
def index():
    return json.dumps({"API RTP Sarah Al Janabi" : "Etape 1"})

# Step 1
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

# Step 2
@app.route('/api/recipes/<slug>.json', methods=['GET'])
def getRecipeBySlug(slug):
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
    #query = "SELECT recipe.id as recipe_id, recipe.slug as slug, recipe.name as recipe_name, user.username, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
    query = "SELECT recipe.id as recipe_id, recipe.name as recipe_name, recipe.slug as slug, user.username, user.last_login as last_login, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
    cursor.execute(query, (slug,))
    rows = cursor.fetchone()

    if rows is None:
        return Response(json.dumps({'code' : 404, 'message' : 'not found'}), 404, {'Content-Type' : 'Application/json'})

    data = {};
    data['id'] = rows['recipe_id']
    data['name'] = rows['recipe_name']
    data['slug'] = rows['slug']
    data['user'] = {}
    data['user']['username'] = rows['username']
    data['user']['id'] = rows['user_id']
    data['user']['last_login'] = rows['last_login'].strftime("%Y-%m-%d %H:%M:%S")

    return Response(json.dumps(
             {
                "code": 200,
                "message": "ok",
                "datas": data
              }), 200, {
              'Content-Type': 'Application/json'
        })

# Step 3
@app.route('/api/recipes/<slug>/steps.json', methods=['GET'])
def getStepsForRecipe(slug):
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
    query = "SELECT step FROM recipes__recipe WHERE slug = %s LIMIT 1;"
    cursor.execute(query, (slug,))
    row = cursor.fetchone()

    if row is None:
        return Response(json.dumps({'code' : 404, 'message' : 'not found'}), 404, {'Content-Type': 'Application/json'})

    steps_load = loads(row['step'].encode(), array_hook=OrderedDict)
    res = []

    for index in steps_load:
        res.append(steps_load[index].decode('utf-8'))

    responseFinal =json.dumps({
        'code' : 200,
        'message' : 'ok',
        'datas' : res
    })
    return Response(responseFinal, 200, {'Content-Type': 'Application/json'})

# Step 4
@app.route('/api/recipes.json', methods=['POST'])
def createRecipe():
    conn = getConnector()
    if not conn:
        return Response(json.dumps(
            {
                "code":500,
                "message" : "no connector"
            }), 500, {
            'Content-Type': 'Application/json'
        })

    cursor = conn.cursor(dictionary=True)

    # Si le mot de passe ne correspond a aucun user en base
    userpass = request.headers.get('Authorization', default = None)
    if (userpass is None):
        return Response(json.dumps({'code' : 401, 'message': 'Unauthorized'}), 401, {'Content-Type': 'Application/json'})

    check_user_query = "SELECT id, username, last_login FROM users__user WHERE password = %s LIMIT 1;"
    cursor.execute(check_user_query, (userpass,))
    row_user = cursor.fetchone()
    if row_user is None:
        return Response(json.dumps({'code' : 403, 'message': 'Invalid Password'}), 403, {'Content-Type': 'Application/json'})

    user_id = row_user['id']

    # Récupération des données du formulaire
    post_data = request.form
    steps = post_data.getlist('step[]')
    name = post_data.get('name', default = None)
    if name is None:
        return Response(json.dumps({'code' : 400, 'message': 'Bad Request', 'datas' : []}), 400, {'Content-Type': 'Application/json'})
    slug = post_data.get('slug', default = None)

    # Si le slug est précisé, je vérifie qu'une recette avec le meme slug n'existe pas
    if slug is not None:
        check_slug_query = "SELECT slug FROM recipes__recipe WHERE slug = %s;"
        cursor.execute(check_slug_query, (slug,))
        row = cursor.fetchone()
        if row is not None:
            return Response(json.dumps({'code' : 400, 'message' : 'Bad Request', 'datas': []}), 400, {'Content-Type': 'Application/json'})
    # Si le slug nest pas précisé, je génère un slug a partir du nom.
    else:
        slug = slugify(name)
        check_slug_query = "SELECT slug FROM recipes__recipe WHERE slug = %s;"
        cursor.execute(check_slug_query, (slug,))
        row = cursor.fetchone()
        # Si le slug généré existe déjà, je rajoute des caracteres aleatoires apres le slug généré
        if row is not None:
            slug = name + '-' + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))


    # Sérialisation des étapes pour les insérer en base
    steps_s = serialize(steps)
    # Insertion en base de données de la nouvelle recette
    create_query = "INSERT INTO recipes__recipe(name, slug, step, user_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(create_query, (name, slug, steps_s, user_id,))
    conn.commit()

    id = cursor.lastrowid
    cursor.close()

    responseData = json.dumps({
        'code' : 201,
        'message' : 'Created',
        'datas' : {
            'id' : id,
            'name' : name,
            'slug' : slug,
            'user' : {
                'username' : row_user['username'],
                'last_login' : row_user['last_login'].strftime('%Y-%m-%dT%H:%M:%S %z'),
                'id' : user_id
            },
            'slug' : slug,
            'step' : steps
        }
    })

    return Response(responseData, 201, {'Content-Type' : 'Application/json'})

# Step 5
@app.route('/api/recipes/<slug>.json', methods=['PUT'])
def updateRecipeBySlug(slug):
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
    query = "SELECT recipe.id as recipe_id, recipe.user_id as user_id FROM recipes__recipe recipe  WHERE slug = %s LIMIT 1;"
    cursor.execute(query, (slug,))
    rows = cursor.fetchone()

    if rows is None:
        return Response(json.dumps({'code' : 404, 'message' : 'not found', 'data' : {}}), 404, {'Content-Type' : 'Application/json'})

    userpass = request.headers.get('Authorization', default = None)
    if (userpass is None):
        return Response(json.dumps({'code' : 401, 'message': 'Unauthorized', 'data' : {}}), 401, {'Content-Type': 'Application/json'})

    check_user_query = "SELECT id, username, last_login FROM users__user WHERE password = %s LIMIT 1;"
    cursor.execute(check_user_query, (userpass,))
    row_user = cursor.fetchone()
    if row_user is None:
        return Response(json.dumps({'code' : 403, 'message': 'Invalid Password', 'data' : {}}), 403, {'Content-Type': 'Application/json'})

    user_id = row_user['id']
    if rows['user_id'] != row_user['id'] :
        return Response(json.dumps({'code' : 403, 'message': 'Invalid Password !', 'data' : {}}), 403, {'Content-Type': 'Application/json'})


    userdata = request.form
    newname = userdata.get('name', default = None)
    newslug = userdata.get('slug', default = None)
    newstep = userdata.getlist('step[]')

    data = OrderedDict();
    if newname is not None :
        data['name'] = newname
    if newname == '' :
        return Response(json.dumps({'code' : 400, 'message': 'Bad Request', 'datas' : []}), 400, {'Content-Type': 'Application/json'})
    if newslug == '' :
        return Response(json.dumps({'code' : 400, 'message': 'Bad Request', 'datas' : []}), 400, {'Content-Type': 'Application/json'})

    if newslug is not None :
        data['slug'] = newslug
        #On vérifie que le new slug n'est pas déjà pris
        checknewslugquery = "SELECT recipe.id FROM recipes__recipe recipe WHERE slug = %s LIMIT 1;"
        cursor.execute(checknewslugquery, (newslug,))
        if (cursor.fetchone() is not None) :
            return Response(json.dumps({'code' : 400, 'message' : 'bad request', 'data' : {}}), 400, {'Content-Type': 'Application/json'})

    if newstep is not None :
        data['step'] = serialize(newstep)

    strquery = ''
    params = {}

    for key, value in data.items():
        if (len(strquery) > 0):
            strquery = strquery + ', '
        strquery = strquery + key + ' = %(' +  key + ')s'
        params[key] = value

    params['original_slug'] = slug

    updatequery = "UPDATE recipes__recipe SET " + strquery + " WHERE slug = %(original_slug)s"
    print(updatequery)
    cursor.execute(updatequery, params)
    conn.commit()

    slug = params.get('slug', None)
    if ( slug is None ) :
        slug = params['original_slug']


    query = "SELECT recipe.id as recipe_id, recipe.name as recipe_name, recipe.slug as slug, recipe.step FROM recipes__recipe recipe WHERE slug = %s LIMIT 1;"
    cursor.execute(query, (slug,))
    rows = cursor.fetchone()

    if rows is None:
        return Response(json.dumps({'code' : 500, 'message' : 'Erreur imprévue'}), 500, {'Content-Type' : 'Application/json'})

    data = {};
    data['id'] = rows['recipe_id']
    data['name'] = rows['recipe_name']
    data['slug'] = rows['slug']

    steps_load = loads(rows['step'].encode(), array_hook=OrderedDict)
    res = []
    for index in steps_load:
        res.append(steps_load[index].decode('utf-8'))

    data['step'] = res

    return Response(json.dumps(
             {
                "code": 200,
                "message": "ok",
                "datas": data
              }), 200, {
              'Content-Type': 'Application/json'
        })

# Step 6
@app.route('/api/recipes/<slug>.json', methods=['DELETE'])
def deleteRecipeBySlug(slug):
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


    # Si le mot de passe ne correspond a aucun user en base
    userpass = request.headers.get('Authorization', default = None)
    if (userpass is None):
        return Response(json.dumps({'code' : 401, 'message': 'Unauthorized'}), 401, {'Content-Type': 'Application/json'})

    check_user_query = "SELECT id, username, last_login FROM users__user WHERE password = %s LIMIT 1;"
    cursor.execute(check_user_query, (userpass,))
    row_user = cursor.fetchone()
    if row_user is None:
        return Response(json.dumps({'code' : 403, 'message': 'Invalid Password'}), 403, {'Content-Type': 'Application/json'})


    user_id = row_user['id']

    #query = "DELETE recipe.id as recipe_id, recipe.slug as slug, recipe.name as recipe_name, user.username, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
    #query = "DELETE recipe.id as recipe_id, recipe.name as recipe_name, recipe.slug as slug, user.username, user.last_login as last_login, user.id as user_id FROM recipes__recipe recipe INNER JOIN users__user user ON user.id = recipe.user_id WHERE slug = %s LIMIT 1;"
    query = "SELECT recipe.id, recipe.user_id as user_id FROM recipes__recipe recipe  WHERE slug = %s LIMIT 1;"
    cursor.execute(query, (slug,))
    row_recipe = cursor.fetchone();

    if row_recipe is None :
	#erreur pas de recette avec slug
        return Response(json.dumps({'code' : 400, 'message': 'Bad Request'}), 400, {'Content-Type': 'Application/json'})

    if row_recipe['user_id']  != user_id:
	#erreur forbidden
        return Response(json.dumps({'code' : 403, 'message': 'Invalid Password'}), 403, {'Content-Type': 'Application/json'})

    dlquery = "DELETE recipes__recipe WHERE id = %d"
    cursor.execute(dlquery, (row_recipe[id],))
    rows = cursor.fetchone()
    conn.commit()

    return Response(json.dumps(
             {
                "code": 200,
                "message": "success",
                "datas":{
                    'id' : row_recipe['id']
		}
              }), 200, {
              'Content-Type': 'Application/json'
})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
