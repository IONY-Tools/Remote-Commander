import flask
import os
import subprocess
from flask import render_template, url_for, request
from dotenv import load_dotenv
from io import StringIO
from contextlib import redirect_stdout

load_dotenv()

app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.get("/")
def index():
    return f"Remote-Commander is running</br>Version: {os.getenv('VERSION')}</br>PC Name: {os.environ['COMPUTERNAME']}"

@app.post("/cmd")
def exec_cmd():
    SECRET = request.form["secret"]
    CMD = request.form["cmd"]
    if SECRET == os.getenv("APPLICATION_SECRET"):
        print(CMD)
        output = subprocess.check_output(CMD, shell=True)
        return output.decode("utf-8")
    else:
        return "Invalid Secret Passed"

@app.post("/restart_server")
def restart_server():
    SECRET = request.form["secret"]
    if SECRET == os.getenv("APPLICATION_SECRET"):
        os.system("shutdown /r")
    else:
        return "Invalid Secret Passed"


def run():
    app.run(host="0.0.0.0", port=os.getenv("WEBSERVER_PORT"))