import os


import os
import subprocess
import redis

# To start the reccomender we need to 
    # 1. start redis
    # 2. run and save the model
    # 3. run flask

def _check_redis():
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    r.ping()

def _start_redis():
    if not _check_redis:
        pass

def _test():
    process = subprocess.Popen(['docker','container', 'ps', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(out)

if __name__ == "__main__":
    _test()