import os
from utils.ws import run
from dotenv import load_dotenv
from multiprocessing import Process
from time import sleep as wait
from utils.msg import MSGHandler

logger = MSGHandler()

load_dotenv()

if os.getenv("APPLICATION_SECRET") == "":
    print("PLEASE SETUP YOUR .ENV FILE FOR APPLICATION SECRET. MAKE SURE IT MATCHES ON ALL MACHINES.")
    exit()

def runner():
    server = Process(target=run)
    server.start()

if __name__ == "__main__":
    runner()
    logger.success("Webserver successfully started.")