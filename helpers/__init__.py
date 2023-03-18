import string
import random

def randomString(length):
    randString = ''.join(random.choices(string.ascii_lowercase +string.ascii_uppercase, k=length))
    return str(randString)