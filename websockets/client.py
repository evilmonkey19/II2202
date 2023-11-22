from websocket import create_connection
import time
import random
import datetime
from multiprocessing import Process

def on_message(ws, message):
    print("HOLAAAA")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def run_instance():
    ws = create_connection("ws://localhost:3549/")
    i = 0
    while i < 1000:
        time.sleep(1)
        value = hash(random.random())
        ws.send(f"i: {hash(random.random())}")
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
        print(f"Sent message {value} : {current_time}")
        i += 1
    ws.close()

if __name__ == "__main__":
    n = 10000
    processes = [Process(target=run_instance) for _ in range(n)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()