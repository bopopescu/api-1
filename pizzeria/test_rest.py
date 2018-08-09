import mysql.connector
import json

from flask import Flask
from flask import request
from flask import make_response
from flask import Response
from mysql.connector import MySQLConnection
from mysql.connector import Error

app = Flask(__name__, template_folder='templates')

def getConnector():
	try:
		conn = mysql.connector.connect(host='localhost',
									   database='pizzeria',
									   user='root',
									   password='qwerty1234')
		if conn.is_connected():
			print('Connected to MySQL database')
			return conn
	except Error as e:
		print(e)
		return False

@app.route('/')
def index():
	return 'Hello world!'


try:
    connection = mysql.connector.connect(host='localhost',
                             database='api',
                             user='root',
                             password='25092015')
    if connection.is_connected():
       db_Info = connection.get_server_info()
       print("Connected to MySQL database... MySQL Server version on ",db_Info)
       cursor = connection.cursor()
       cursor.execute("select database();")
       record = cursor.fetchone()
       print ("Your connected to - ", record)
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# def getConnector():
# 	try:
# 		conn = mysql.connector.connect(host='localhost',
# 									   database='pizzeria',
# 									   user='root',
# 									   password='qwerty1234')
# 		if conn.is_connected():
# 			print('Connected to MySQL database')
# 			return conn
# 	except Error as e:
# 		print(e)
# 		return False

@app.route('/')
def index():
	return 'Hello world!'

@app.route('/toto')
def toto():
	print(request)
	return 'Hello worldcdfcqsdf!'

@app.route('/ingredients/<string:ing>', methods=['POST'])
def addIngredient(ing):
	query = "INSERT INTO ingredient(name) " \
			"VALUES(%s,%s)"
	args = ("name", ing)
	print(ing)
	conn = getConnector()
	if not conn:
		return Response(json.dumps({"code":200, "message" : "no connector"}), 200)
	cursor = conn.cursor()
	cursor.execute("SELECT * from ingredient WHERE name LIKE '%" + ing + "%'")
	row = cursor.fetchone()
	print(row)
	if row is not None:
		return Response(json.dumps({"code":200, "message" : "ingredient already exists"}), 200)
	print("INSERT INTO ingredient(name) VALUES(" + ing + ")")
	cursor.execute('INSERT INTO ingredient (name) VALUES("' + ing + '")')
	# cursor.execute(query, args)
	if cursor.lastrowid:
		print('last insert id', cursor.lastrowid)
	conn.commit()
	cursor.close()
	conn.close()
	return Response(json.dumps({"code":200, "message" : "ingredient " + ing + " successfully added"}), 200)

@app.route('/ingredients', methods=['GET'])
def getIngredients():
	conn = getConnector()
	if not conn:
		return Response(json.dumps({"code":200, "message" : "no connector"}), 200)
	cursor = conn.cursor()
	cursor.execute("SELECT * from ingredient")
	rows = cursor.fetchall()
	datas = {}
	for row in rows:
		print(row)
		datas[row[0]] = row[1]
	return Response(json.dumps({"code":200, "message" : "successfully got ingredient", "datas" : datas}), 200)

@app.route('/ingredients', methods=['POST'])
def addIngredients():
	conn = getConnector()
	cursor = conn.cursor()
	query = 'INSERT INTO ingredient (name) VALUES '
	print(request)
	print(request.args)
	print(request.get_json())
	args = request.get_json()
	print(args['Ingredients'])
	s = ""
	a = []
	s1 = ""
	for iding, ing in args['Ingredients'].iteritems():
		print(iding + " : " + ing)
		s += ing + " "
		a.append(str(ing))
		#",".join()
	print(s)
	print(a)
	print(",".join(s))
	print('"), ("'.join(a))
	newS = '"), ("'.join(a)
	newS = '("' + newS + '")'
	print(newS)
	query += newS
	print(query)
	cursor.execute(query)
	conn.commit()
	cursor.close()
	conn.close()
	return Response(json.dumps({"code":200, "message" : "successfully got ingredient", "datas" : args['Ingredients']}), 200)

@app.route('/pizzas', methods=['POST'])
def addOrder():
	conn = getConnector()
	cursor = conn.cursor()
	queryP = "INSERT INTO pizza (name, sexe, address, phone, comments) VALUES ("
	print(request.get_json())
	args = request.get_json()
	print(args)
	ingredients = args['pizza']['Ingredients']
	del(args['pizza']['Ingredients'])
	print(ingredients)
	print(args)
	pizza = args['pizza']
	queryP += '"' + pizza['name'] + '", ' + '"' + pizza['sexe'] + '", ' + '"' + pizza['address'] + '", ' + '"' + pizza['phone'] + '", ' + '"' + pizza['comments'] + '")'
	print(queryP)
	cursor.execute(queryP)
	lastPizzaId = cursor.lastrowid
	print(lastPizzaId)
	conn.commit()
	ingId = []

	for ing in ingredients:
		cursor.execute("SELECT id from ingredient WHERE name LIKE '%" + ing + "%'")
		row = cursor.fetchone()
		if row is None:
			cursor.execute('INSERT INTO ingredient (name) VALUES("' + ing + '")')
			ingId.append(cursor.lastrowid)
			conn.commit()
		else:
			ingId.append(row[0])

	print(ingId)
	for ident in ingId:
		cursor.execute('INSERT INTO pizza_ingredient (pizza, ingredient) VALUES (' + str(lastPizzaId) + ', ' + str(ident) + ')')
		conn.commit()
	conn.close()
	cursor.close()
	return 'Hello'

if __name__ == '__main__':
    app.run(debug=True)
    from werkzeug.serving import run_simple

    application.debug = True
    run_simple('0.0.0.0', 000, application, use_reloader=True, use_debugger=True)