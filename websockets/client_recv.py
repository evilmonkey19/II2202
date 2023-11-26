from websocket import create_connection
import datetime
from multiprocessing import Process
import argparse
import os

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
    value = ''
    while True:
        value = ws.recv()
        if value == b'close':
            break
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
        timings.append(f'{value.decode("utf-8")},{current_time}')
    ws.close()
    with open(f"../results/websockets/clients/{n}/client_recv_{instance_name}.csv", "w") as f:
        f.write("\n".join(timings))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('n', metavar='N', type=int, help='an integer for the number of processes')

    args = parser.parse_args()

    os.makedirs(f"../results/websockets/clients/{args.n}", exist_ok=True)

    processes = [Process(target=run_instance, args=(f"{i}",args.n)) for i in range(args.n)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()