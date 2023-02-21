import flask
import sqlite3
import os
from flask import Flask, url_for, redirect, request, render_template, make_response
from dotenv import load_dotenv

load_dotenv()

app = Flask()

@app.get("/")
def index():
    return

@app.get("/auth/login")
def login():
    return

@app.post("/api/v1/auth/login")
def auth_login():
    return

@app.post("/api/v1/users/create")
def user_create():
    return

@app.delete("/api/v1/users/delete")
def user_delete():
    return

@app.get("/panel")
def panel():
    return

@app.post("/api/v1/devices/add")
def device_add():
    return

@app.delete("/api/v1/devices/remove")
def remove_device():
    return

@app.post("/api/v1/users/password_change")
def change_password():
    return



def run():
    app.run(host="0.0.0.0", port=os.getenv("WEBSERVER_PORT"))