from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import time
import random
import datetime
import argparse
import os
import requests

PORT: int = 3501
http_url: str = f"http://localhost:{PORT}/graphql"

def send_query(value: int):
    try: 
        requests.post(http_url, json={
            "query": f"""
                mutation send {{
                    sendMessage(name: "Sender", content: "{value}"){{
                        id
                        name
                        content
                    }}
                }}  
            """
        }, timeout=0.000000001)
    except requests.exceptions.ReadTimeout: 
        pass

def run_instance(instance_name: str, n: int):
    # transport = AIOHTTPTransport(url=http_url)
    # client = Client(transport=transport, fetch_schema_from_transport=True)
    timings = []
    i = 0
    while i < 1000:
        value = hash(random.random())
        send_query(value)
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
        timings.append(f'{value},{current_time}')
        i += 1
    time.sleep(1)
    send_query("close")
    # client.close_sync()
    # client.transport.close()
    with open(f"../results/graphql/clients/{n}/sender_timings.csv", "w") as f:
        f.write("\n".join(timings))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('n', metavar='N', type=int, help='an integer for the number of processes')

    args = parser.parse_args()

    os.makedirs(f"../results/graphql/clients/{args.n}", exist_ok=True)

    run_instance("1", args.n)