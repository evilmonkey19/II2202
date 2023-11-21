import { ApolloClient, InMemoryCache, gql } from '@apollo/client';
import { WebSocketLink } from '@apollo/client/link/ws';

const client = new ApolloClient({
  link: new WebSocketLink({
    uri: `ws://localhost:3501/graphql`,
    options: {
      reconnect: true,
    },
  }),
  cache: new InMemoryCache(),
});

function sendMessage(e) {
  e.preventDefault();
  const input = document.getElementById('messageInput');
  if (input.value) {
    client.mutate({
      mutation: gql`
        mutation {
          addMessage(message: "${input.value}")
        }
      `,
    });
    input.value = '';
  }
  input.focus();
}

document.getElementById('messageForm').addEventListener('submit', sendMessage);

client.subscribe({
  query: gql`
    subscription {
      messageAdded
    }
  `,
}).subscribe({
  next: (data) => {
    const li = document.createElement('li');
    li.textContent = data.data.messageAdded;
    document.getElementById('messageList').appendChild(li);
  },
});
