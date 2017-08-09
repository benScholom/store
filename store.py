from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189256',
                             password='4XXsiRzcZc',
                             db = 'sql11189256',
                             charset = 'utf8mb4',
                             cursorclass = pymysql.cursors.DictCursor)

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/products")
def products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@get("/category/<id>/products")
def cat_prod_id(id):
    cat_id = id
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products where cat_id  = {}".format(cat_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        return json.dumps({"STATUS": "SUCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({'STATUS': "ERROR", "MSG": "Internal error", "CODE": 500})

@get("/categories")
def cat_list():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCESS", "CATEGORIES": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@route("/category", method = "POST")
def new_name():
    name = request.POST.get("name")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories (cat_id, cat_name) VALUES (0, {})".format(name)
            cursor.execute(sql)
            connection.commit()
            result = cursor.lastrowid()
            return json.dumps({"STATUS":"SUCCESS", "CAT_ID": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Does not work"})


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=7000)
