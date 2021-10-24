from flask import Flask, jsonify, request
import hashlib
from datetime import date
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect, generate_csrf

import sqlite3
from flask import g

DATABASE = 'database.db'

app = Flask(__name__, static_folder="public")
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
def create_tables():
    with app.app_context():
        tables = [
            """CREATE TABLE IF NOT EXISTS Users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    UNIQUE (email)
                )
                """,
            """CREATE TABLE IF NOT EXISTS Datas(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
        ]
        db = get_db()
        cursor = db.cursor()
        for table in tables:
            cursor.execute(table)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)

# database

class User(UserMixin):
    ...

def get_user(user_id: int):
    user = query_db('select * from Users where id = ?',
                [user_id], one=True)
    return user


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user[0]
        
        return user_model
    return None


@app.route("/api/ping", methods=["GET"])
def home():
    return jsonify({"ping": "pong!"})


@app.route("/api/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    hashPassword = hashlib.md5(password.encode()).hexdigest()

    user = query_db('select * from Users where email = ? and password = ?',
                [email,hashPassword], one=True)
    
    if user is not None:
        user_model = User()
        user_model.id = user[0]
        login_user(user_model)

        response = {
            "status":"ok",
            
        }    
    else:
        response = {
            "status":"error",
            "message":"invalid-login-request",
        }
    return jsonify(response)

@app.route("/api/update", methods=["POST"])
@login_required
def update():
    data = request.json
    oldPassword = data.get("oldPassword")
    password = data.get("password")

    hashOldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
    hashNewPassword = hashlib.md5(password.encode()).hexdigest()

    user = get_user(current_user.id)
    if (hashOldPassword != user[2]): #password doesn't match
        return jsonify({"error": 1, "message": "Old password incorrect!"})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE Users SET password= ? WHERE id = ?",(hashNewPassword,current_user.id))   
        db.commit() 
        return jsonify({"error":0,"message": "Success to update"})
    except sqlite3.Error as error:
        db.rollback()
        return jsonify({"error":2,"message": "Failed to update"})


@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.json
    content = data.get("name")
    try:
        db = get_db()
        cursor = db.cursor()
        currentdate = date.today()
        cursor.execute("INSERT into Datas ( name,date,status) values (?,?,?)",(content,currentdate,"success"))   
        db.commit() 
        return jsonify({"status":"ok"})
    except sqlite3.Error as error:
        db.rollback()
        return jsonify({"status":"error","message": "Failed to upload"})

@app.route("/api/datalist", methods=["POST"])
def uploadList():
    try:
        data = query_db('select * from Datas ')
        return jsonify({"status":"ok","data":data})
    except sqlite3.Error as error:
        return jsonify({"status":"error","message": "Failed to get list"})
  

@app.route("/api/signup", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    hashPassword = hashlib.md5(password.encode()).hexdigest()

    user = query_db('select * from Users where email = ?',
                [email], one=True)
    if user is not None:
        return jsonify({"status":"error","message": "User already exists"})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT into Users (email, password) values (?,?)",(email,hashPassword))   
        db.commit() 
        return jsonify({"status":"ok"})
    except sqlite3.Error as error:
        db.rollback()
        return jsonify({"status":"error","message": "Failed to register"})
 

@app.route("/api/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"email": user[1]})


@app.route("/api/getsession")
def check_session():
    
    if current_user.is_authenticated:
        user = get_user(current_user.id)
        
        return jsonify({"login": True,"username":user[1]})

    return jsonify({"login": False})


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, host="0.0.0.0")
