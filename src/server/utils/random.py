import random
import string

class Random:
    def __init__(self):
        super()

    def random_string(self, length: int) -> str:
        gen_string = ""
        for i in range(length):
            gen_string += random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits)

        return gen_string

    def random_number(self, max: int) -> int:
        return random.randint(1, max)
    