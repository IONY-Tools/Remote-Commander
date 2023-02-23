import colorama
from colorama import Fore, Back

class MSGHandler:
    def __init__(self):
        return

    def info(msg):
        print(Back.CYAN+Fore.WHITE+" INFO "+Fore.RESET+Back.RESET+" "+msg) 

    def warning(msg):
        print(Back.YELLOW+Fore.WHITE+" WARNING "+Fore.RESET+Back.RESET+" "+msg) 

    def error(msg):
        print(Back.RED+Fore.WHITE+" ERROR "+Fore.RESET+Back.RESET+" "+msg) 

    def success(msg):
        print(Back.GREEN+Fore.WHITE+" SUCCESS "+Fore.RESET+Back.RESET+" "+msg)