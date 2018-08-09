
import json
import sqlite3

from flask import Flask
from flask import request
from flask import make_response
from flask import Response

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
		print(e)
		return False

@app.route('/', methods=['GET'])
def index():
	return 'Hello world toto!'

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/toto')
def toto():
	print(request)
	return 'Hello world!'

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


conn = sqlite3.connect('pizzeria.sql')
conn.row_factory = dict_factory
cur = conn.cursor()
results = cur.execute(query, to_filter).fetchall()

return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)