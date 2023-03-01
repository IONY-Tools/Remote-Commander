import flask
import sqlite3
import os
import logging
import string as letters
import random
import base64
import requests
from flask import Flask, url_for, redirect, request, render_template, make_response, send_file
from dotenv import load_dotenv
from utils.database import DBConnection
from utils.msg import MSGHandler
from libgravatar import Gravatar
from flask_cors import CORS

database = DBConnection("databases\Remote-Commander.db")

load_dotenv()

app = Flask(__name__, static_url_path="/public" ,template_folder=os.getcwd() + "\\public\\html\\", static_folder=os.getcwd() + "\\public\\")
logger = logging.getLogger("werkzeug")
logger.disabled = True
CORS(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True

MessageHandler = MSGHandler()

def gen_session(username):
    chars = letters.ascii_lowercase+letters.ascii_uppercase+letters.digits
    part1 = base64.b64encode(username.encode("utf-8"))
    string = ""
    for i in range(50):
        string += random.choice(chars)
    part2 = base64.b64encode(string.encode("utf-8"))
    string = ""
    for i in range(25):
        string += random.choice(chars)
    part3 = base64.b64encode(string.encode("utf-8"))
    return (part1.decode("utf-8") + "." + part2.decode("utf-8") + "." + part3.decode("utf-8")).replace("=", "")

def gen_uuid():
    uuid = ""
    chars = letters.ascii_lowercase+letters.ascii_uppercase+letters.digits
    for i in range(8):
        uuid += random.choice(chars)
    uuid += "-"
    for i in range(24):
        uuid += random.choice(chars)
    uuid += "-"
    for i in range(12):
        uuid += random.choice(chars)
    return uuid

@app.get("/")
def index():
    if not 'session' in request.cookies:
        return redirect(url_for("login"))
    else:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if len(qry) == 0:
            return redirect(url_for("login"))
        else:
            return redirect(url_for("panel"))

@app.get("/auth/login")
def login():
    if 'session' in request.cookies:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if not len(qry) == 0:
            return redirect(url_for("panel"))
    
    return render_template("auth.login.html")

@app.post("/api/v1/auth/login")
def auth_login():
    username = request.form["username"]
    password = request.form["password"]
    qry = database.cursor().execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'").fetchall()
    if not len(qry) == 0:
        resp = make_response(redirect(url_for("panel")))
        resp.set_cookie("session", qry[0][8])
        return resp
    else:
        return redirect(url_for("login"))

@app.post("/api/v1/users/create")
def user_create():
    if not 'session' in request.cookies:
        return redirect(url_for("login"))
    else:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if len(qry) == 0:
            return redirect(url_for("login"))
    
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    uuid = gen_uuid()
    session = gen_session()
    admin = request.form["admin"]
    id = random.randint(1, 999999)

    database.cursor().execute(f"INSERT INTO users VALUES ('{uuid}', '{username}', '{email}', '{firstname}', '{lastname}', '{id}', '{password}', '{admin}', '{session}')")
    database.commit()

    return redirect(url_for("panel"))    

@app.delete("/api/v1/users/delete")
def user_delete():
    return

@app.get("/panel")
def panel():
    pfp = ""
    user = {}
    if not 'session' in request.cookies:
        return redirect(url_for("login"))
    else:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if len(qry) == 0:
            return redirect(url_for("login"))
        pfp = Gravatar(qry[0][2]).get_image()
        user["uuid"] = qry[0][0]
        user["username"] = qry[0][1]
        user["email"] = qry[0][2]
        user["first_name"] = qry[0][3]
        user["last_name"] = qry[0][4]
        user["id"] = qry[0][5]
        user["admin"] = qry[0][7]
    statistics = {"online": 0}
    return render_template("dashboard.html", profile_pic=pfp, user=user,statistics=statistics)

@app.get("/devices")
def devices():
    pfp = ""
    if not 'session' in request.cookies:
        return redirect(url_for("login"))
    else:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if len(qry) == 0:
            return redirect(url_for("login"))
        pfp = Gravatar(qry[0][2]).get_image()
    qry = database.cursor().execute("SELECT * FROM devices").fetchall()
    dev = []
    for i in qry:
        req = requests.get("http://"+i[1]+":"+str(i[2])+"/ping", data = {"secret": i[4]})
        i = list(i)
        if req.text == "OK":
            i.append("up")
        else:
            i.append("down")
        dev.append(i)
    return render_template("devices.html", profile_pic=pfp, devices=dev)

@app.post("/api/v1/devices/add")
def device_add():
    return

@app.delete("/api/v1/devices/remove")
def remove_device():
    return

@app.post("/api/v1/users/password_change")
def change_password():
    return

@app.get("/public/<string:filepath>")
def public(filepath):
    return send_file(os.getcwd() + "\\public\\" + filepath)

@app.get("/device/<string:uuid>")
def device_view(uuid):
    pfp = ""
    if not 'session' in request.cookies:
        return redirect(url_for("login"))
    else:
        qry = database.cursor().execute(f"SELECT * FROM users WHERE session='{request.cookies['session']}'").fetchall()
        if len(qry) == 0:
            return redirect(url_for("login"))
        pfp = Gravatar(qry[0][2]).get_image()
    qry = database.cursor().execute(f"SELECT * FROM devices WHERE uuid='{uuid}'").fetchone()
    dev = {
        "uuid": qry[0],
        "ip": qry[1],
        "port": qry[2],
        "nickname": qry[3],
        "secret": qry[4],
        "public_ip": requests.get(f"http://{qry[1]}:{qry[2]}/public_ip", data={"secret":qry[4]}).text
    }
    img = requests.get(f"http://{dev['ip']}:{dev['port']}/screen", data={"secret": dev["secret"]}).text
    url = f'http://{dev["ip"]}:{dev["port"]}/public/'+img
    return render_template("device.manage.html", profile_pic=pfp, device=dev, url=url)

def run():
    MessageHandler.success("Running webserver on port 80...")
    app.run(host="0.0.0.0", port=80)