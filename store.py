from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189256',
                             password='4XXsiRzcZc',
                             db = 'sql11189256',
                             charset = 'utf8mb4',
                             cursorclass = pymysql.cursors.DictCursor,
                             autocommit = True)

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
            print(json.dumps(result))
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@get("/product/<id>")
def get_prod(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT FROM products WHERE id = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS':"SUCCESS", "PRODUCT": result, "CODE": 200 })
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@get("/category/<id>/products")
def cat_prod_id(id):
    cat_id = id
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products where category  = {}".format(cat_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(json.dumps(result))
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
            print(result)
            print(json.dumps(result))
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@route("/category", method = "POST")
def new_name():
    name = request.POST.get("name")
    print(name)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories (name) VALUES ('{}')".format(name)
            cursor.execute(sql)
            result = cursor.lastrowid
            """sql2 = "SELECT id FROM categories WHERE name = ('{}')".format(name)
            result = cursor.execute(sql2)
            print(result)"""
            return json.dumps({"STATUS":"SUCCESS", "CAT_ID": result, "CODE": 201})
    except:
        return json.dumps({"STATUS":"ERROR", "MSG": 'something went wrong'})
    """except Exception as e:
        if str(e) == '200':
            return json.dumps({'STATUS':"ERROR", "MSG": "category already exists"})
        elif str(e) == '400':
            return json.dumps({'STATUS': "ERROR", "MSG": "bad request"})
        elif str(e) == '500':
            return json.dumps({'STATUS': "ERROR", "MSG": "internal error"})"""

@delete('/category/<id>')
def del_cat(id):
    cat_id = id
    try:
        with connection.cursor() as cursor:
            sql2 = "DELETE FROM products WHERE Category = {}".format(cat_id)
            cursor.execute(sql2)
            sql = "DELETE FROM categories WHERE id = {}".format(cat_id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "category deleted successfully", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": 'something went wrong'})

@post('/product')
def add_edit_pro():
    cat_id = request.POST.get('category')
    description = request.POST.get('description')
    price = request.POST.get('price')
    title = request.POST.get('title')
    favorite = request.POST.get('favorite')
    img_url = request.POST.get('img_url')
    id = request.POST.get('id')



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
