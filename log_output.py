import datetime
import time
import random
import string

def gen_random_and_output():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    while True:
        current_datetime = datetime.datetime.now()

        print(str(current_datetime) + " "+ random_string)
        time.sleep(5)

gen_random_and_output()