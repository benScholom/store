from _mysql_exceptions import *
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

#products list
@get("/products")
def products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})
#specific product information
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
#viewing prodicts by category
@get("/category/<id>/products")
def cat_prod_id(id):
    cat_id = id
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products where category  = {}".format(cat_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCESS", "PRODUCTS": result, "CODE": 200})
    except:
        return json.dumps({'STATUS': "ERROR", "MSG": "Internal error", "CODE": 500})
#viewing categories
@get("/categories")
def cat_list():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE": 200})
    except:
        return json.dumps({'STATUS':"ERROR", "MSG": "Internal error", "CODE": 500})

@delete("/product/<id>")
def del_prod(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = {}".format(id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "product deleted successfully", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": 'something went wrong'})

#create a new category, test if category is already present and return specific error if so. Note that the name column is unique
@route("/category", method = "POST")
def new_name():
    name = request.POST.get("name")
    if name == "":
        return json.dumps({"STATUS":"ERROR", "MSG": 'Bad request'})
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories (name) VALUES ('{}')".format(name)
            cursor.execute(sql)
            result = cursor.lastrowids
            return json.dumps({"STATUS":"SUCCESS", "CAT_ID": result, "CODE": 201})
    #test to see if name already taken and ensure that one is entered to begin with
    except:
        return json.dumps({"STATUS":"ERROR", "MSG": 'Internal error'})
    """ except IntegrityError:
            return json.dumps({"STATUS":"ERROR", "MSG": 'Category name already taken'})
        except Error:
            return json.dumps({"STATUS":"ERROR", "MSG": 'Internal error'})"""
#delete a category, also remove all products in that caeogry at the same time
@delete('/category/<id>')
def del_cat(id):
    cat_id = id
    try:
        with connection.cursor() as cursor:
            sql2 = "DELETE FROM products WHERE category = {0}".format(cat_id)
            cursor.execute(sql2)
            sql = "DELETE FROM categories WHERE id = {0}".format(cat_id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "category deleted successfully", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": 'something went wrong'})

@post('/product')
def add_edit_pro():
    cat_id = request.POST.get('category')
    description = request.POST.get('desc')
    price = request.POST.get('price')
    title = request.POST.get('title')
    favorite = request.POST.get('favorite')
    img_url = request.POST.get('img_url')
    attributes = [cat_id, description, price, title, favorite, img_url]
    for a in attributes:
        if a == "":
            return json.dumps({"STATUS": "ERROR", "MSG": 'please fill all fields'})
    if favorite == 'on':
        favorite = True;
    else:
        favorite = False;
    try:
        with connection.cursor() as cursor:
            gid = "SELECT id FROM products WHERE title = '{}'".format(title)
            cursor.execute(gid)
            getid = cursor.fetchall()
            if not cursor.rowcount:
                sql = "INSERT INTO products (category, description, price, title, favorite, img_url) VALUES ({0},'{1}',{2},'{3}',{4},'{5}')".format(cat_id, description, price, title, favorite, img_url)
                cursor.execute(sql)
                return json.dumps({"STATUS": "SUCCESS", "MSG": "product created successfully", "CODE": 201})
            elif cursor.rowcount:
                sql2 = "UPDATE products SET category = {0}, description = '{1}', price = {2}, title = '{3}', favorite = {4}, img_url = '{5}' WHERE id = {6}".format(cat_id, description, price, title, favorite, img_url, int(getid[0]['id']))
                print(sql2)
                cursor.execute(sql2)
                return json.dumps({"STATUS": "SUCCESS", "MSG": "product updated successfully", "CODE": 201})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": 'something went wrong'})


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
