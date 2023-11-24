from websocket import create_connection
import random
import datetime
import argparse
import os
import time

def on_message(ws, message):
    print("HOLAAAA")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def run_instance(instance_name: str, n: int):
    ws = create_connection("ws://localhost:3549/")
    timings = []
    i = 0
    while i < 1000:
        value = hash(random.random())
        ws.send(str(value))
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
        timings.append(f'{value},{current_time}')
        i += 1
    time.sleep(1)
    ws.send('close')
    ws.close()
    with open(f"../results/websockets/clients/{n}/sender_timings.csv", "w") as f:
        f.write("\n".join(timings))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('n', metavar='N', type=int, help='an integer for the number of processes')

    args = parser.parse_args()

    os.makedirs(f"../results/websockets/clients/{args.n}", exist_ok=True)

    run_instance("1", args.n)