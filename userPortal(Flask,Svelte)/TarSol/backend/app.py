from flask import Flask, jsonify, request
import hashlib
import mysql
from dbconn import Conn
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

from flask import g

# from solutions.PhysicianLicenseValidator.main import PhysicianLicenseValidator

print("FOOBAR")
app = Flask(__name__, static_folder="public")
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

def get_db():
    
    conn = Conn()
    cursor = conn.cursor
    
    return conn.conn

def query_db(query, args=(), one=False):
    conn = Conn()
    cursor = conn.cursor

    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    pass

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)

# database

class User(UserMixin):
    ...

def get_user(user_id: int):
    user = query_db('select * from Users where id = %s',
                [user_id], one=True)
    return user


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        print('ok login')
        user_model = User()
        user_model.id = user[0] #[0] means id
        
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

    conn = Conn()
    cursor = conn.cursor
    cursor.execute('select * from Users where email = %s and password = %s',
                [email,hashPassword], multi=False)
    try:
        user = cursor.fetchone()
        if user is not None:
            user_model = User()
            user_model.id = user[0] #[0] means  id
            login_user(user_model)

            response = {
                "status":"ok",
            }
        else:
            response = {
                "status":"error",
                "message":"invalid-login-request",
            }    
    except mysql.connector.errors.InterfaceError as ie:
        raise
    
    cursor.close()
    return jsonify(response)

@app.route("/api/jsonfromexcel", methods=["POST"])
@login_required
def jsonfromexcel():
    data = request.json
    
    response = {'status': data}
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
        conn = Conn()
        cursor = conn.cursor
        cursor.execute("UPDATE Users SET password= ? WHERE id = ?",(hashNewPassword,current_user.id))
        conn.conn.commit() 
        return jsonify({"error":0,"message": "Success to update"})
    except mysql.connector.errors.InterfaceError as ie:
        conn.conn.commit() 
        return jsonify({"error":2,"message": "Failed to update"})


@app.route("/api/upload", methods=["POST"])
@login_required

def upload():

    data = request.json
    values = data.get("data")
    
    print(values)
    conn = Conn()
    cursor = conn.cursor
    #get user
    user = get_user(current_user.id)
    try:
        for value in values: 
            if len(value) > 3: #ignore when value is empty
                cursor.execute("INSERT into Data (user,lic,npi,exp,zip,user_email) values (%s,%s,%s,%s,%s,%s)",(current_user.id,value['licenseNumber'],value['npi'],value['expDate'],value['zipcode'],user[1]))   
            
        conn.conn.commit()    
        
        return jsonify({"status":"ok"})
    except mysql.connector.errors.InterfaceError as error:
        conn.conn.rollback()
        return jsonify({"status":"error","message": "Failed to upload"})
    

@app.route("/api/datalist", methods=["POST"])
def uploadList():
    pass
  

@app.route("/api/signup", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    hashPassword = hashlib.md5(password.encode()).hexdigest()

    conn = Conn()
    cursor = conn.cursor
    cursor.execute('select * from Users where email = %s',
                [email], multi=False)
    user = cursor.fetchone()
    if user is not None:
        return jsonify({"status":"error","message": "User already exists"})
    
    try:
        cursor.execute("INSERT into Users (email, password) values (%s,%s)",(email,hashPassword))   
        conn.conn.commit() 
        return jsonify({"status":"ok"})
    except mysql.connector.errors.InterfaceError as error:
        conn.conn.rollback()
        return jsonify({"status":"error","message": "Failed to register"})
 

@app.route("/api/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"email": user[1]})


@app.route("/api/getsession")
def check_session():
    print('getsess')
    if current_user.is_authenticated:
        print('isauth')
        user = get_user(current_user.id)
        return jsonify({"login": True,"username":user[1]})
    print('noauth')
    return jsonify({"login": False})


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})


if __name__ == "__main__":
    #create_tables()
    app.run(debug=True, host="0.0.0.0")
