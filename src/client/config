import colorama
import sys
from colorama import Fore, Back

commands = {
    "rc:create:user": {
        "callback": "create_user()"
    }
}

def info(msg):
    print(Back.CYAN+Fore.WHITE+" INFO "+Fore.RESET+Back.RESET+" "+msg) 

def warning(msg):
    print(Back.YELLOW+Fore.WHITE+" WARNING "+Fore.RESET+Back.RESET+" "+msg) 

def error(msg):
    print(Back.RED+Fore.WHITE+" ERROR "+Fore.RESET+Back.RESET+" "+msg) 

def prompt(msg, default: str = None) -> str:
    endpart = Fore.WHITE+":"
    if default != None:
        endpart = Fore.WHITE+" ["+Fore.YELLOW+f"{default}"+Fore.WHITE+"]:"
    print(Fore.GREEN+msg+Fore.WHITE+endpart)
    result = input("> ")
    if result == "":
        if default == None:
            error("Fail!")
            exit()
        else: 
            result = default
    return result

def create_user():
    print(prompt("First Name"))
    exit()

def parse():
    args = sys.argv[1:]
    try:
        eval(commands[args[0]]["callback"])
    except:
        error("Command not found.")

parse()