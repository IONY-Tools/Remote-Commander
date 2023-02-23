import flask
import os
import subprocess
import pyautogui
import logging
import sys
from flask import render_template, url_for, request, send_file
from dotenv import load_dotenv
from io import StringIO
from contextlib import redirect_stdout
from utils.random import Random

sys.path.append("src\server\screenshots")

print(os.getcwd())


load_dotenv()

random = Random()

app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

logger = logging.getLogger("werkzeug")
logger.disabled = True

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

@app.get("/screen")
def screenshot():
    SECRET = request.form["secret"]
    if SECRET == os.getenv("APPLICATION_SECRET"):
        file_name = random.random_string(16)
        Screenshot = pyautogui.screenshot()
        Screenshot.save(rf'{os.getenv("SCREENSHOT_DIR")}{file_name}.png')
        return send_file(rf'{os.getenv("SCREENSHOT_DIR")}{file_name}.png')
    else:
        return "Invalid Secret Passed"

def run():
    app.run(host="0.0.0.0", port=os.getenv("WEBSERVER_PORT"))