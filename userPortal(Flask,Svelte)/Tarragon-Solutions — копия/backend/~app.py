from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect, generate_csrf

app = Flask(__name__, static_folder="public")
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)

# database
users = [
   {
        "id": 1,
        "username": "test",
        "password": "test",
    },
    {
        "id": 2,
        "username": "admin",
        "password": "admin",
    },
    {
        "id": 3,
        "username": "yaroslav",
        "password": "yaroslav",
    }
]


class User(UserMixin):
    ...


def get_user(user_id: int):
    for user in users:
        if int(user["id"]) == int(user_id):
            return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user["id"]
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
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            user_model = User()
            user_model.id = user["id"]
            login_user(user_model)
            return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"username": user["username"]})


@app.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})

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
        db.rollback();
        return jsonify({"error":2,"message": "Failed to update"})
    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
