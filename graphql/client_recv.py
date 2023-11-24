from graphql_client import GraphQLClient
import datetime
from multiprocessing import Process, Manager
import argparse
import os, glob, time

PORT: int = 3501
http_url: str = f"http://localhost:{PORT}/graphql"
ws_url: str = f"ws://localhost:{PORT}/graphql"

subscription_query: str = """
subscription receive {
     receiveMessage{
          id
          name
          content
     }
}
"""

finished: list[str] = ['hola']

def write_results(n: int, timings):
     result = {}
     for timing in timings:
          split_timing = timing.split(',')
          _id = split_timing[0]
          if _id not in result:
               result[_id] = []
          result[_id].append([split_timing[1], split_timing[2]])
     i = 0
     for _id, results in result.items():
          with open(f"../results/graphql/clients/{n}/client_recv_{i}.csv", "w") as f:
               f.write("\n".join([",".join(result) for result in results]))
          i += 1

def callback(_id, value, all_timings, finished):
     """
     Callback function.
     """
     received = value['payload']['data']['receiveMessage']['content']
     if received == 'close':
          finished.append(_id)
     else:
          current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
          all_timings.append(f'{_id},{received},{current_time}')


def run_instance(all_timings, finished):
     with GraphQLClient(ws_url) as client:
          sub_id = client.subscribe(subscription_query, callback=lambda _id, value: callback(_id, value, all_timings, finished))
          while sub_id not in finished:
               pass
          client.stop_subscribe(sub_id)
     return

if __name__ == "__main__":
     parser = argparse.ArgumentParser(description='Process some integers.')
     parser.add_argument('n', metavar='N', type=int, help='an integer for the number of processes')

     args = parser.parse_args()

     os.makedirs(f"../results/graphql/clients/{args.n}", exist_ok=True)
     global n
     n = args.n
     with Manager() as manager:
          all_timings = manager.list()
          finished = manager.list()

          processes = [Process(target=run_instance, args=(all_timings, finished,)) for _ in range(args.n)]
          for p in processes:
               p.start()

          for p in processes:
               p.join()

          all_timings = list(all_timings)
          write_results(args.n, all_timings)