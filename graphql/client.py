from graphql_client import GraphQLClient
from python_graphql_client import GraphqlClient
import time
from colorama import Fore, Style

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
mutation_query:str = """
mutation send {
     sendMessage(name: "User", content: "Hello"){
        id
        name
        content
     }
}
"""


def callback(_id, data):
     """
     Callback function.
     """
     msg = data['payload']['data']['receiveMessage']
     print(f"id: {Fore.YELLOW}{msg['id']}{Style.RESET_ALL}, name: '{Fore.GREEN}{msg['name']}{Style.RESET_ALL}', content: '{Fore.GREEN}{msg['content']}{Style.RESET_ALL}'")


def make_query(query: str):
    """
    Make the query.
    """
    request = request.post(http_url, json={'query': query})


client = GraphqlClient(endpoint=http_url)

with GraphQLClient(ws_url) as subscriptions_client:
     sub_id = subscriptions_client.subscribe(subscription_query, callback=callback)
     try:
          while True:
               client.execute(query=mutation_query)
               time.sleep(1)
     except KeyboardInterrupt:
          subscriptions_client.stop_subscribe(sub_id)