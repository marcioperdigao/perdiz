import subprocess
from multiprocessing import Process
import os

def run_websocket():
    subprocess.run(["python3","game.py"])

def run_gunicorn():
    subprocess.run(["python3","server.py"])

if __name__=="__main__":
    websocket_process = Process(target=run_websocket)
    websocket_process.start()

    gunicorn_process = Process(target=run_gunicorn)
    gunicorn_process.start()

    websocket_process.join()
    gunicorn_process.join()
     
