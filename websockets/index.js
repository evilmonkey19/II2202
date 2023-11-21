import express from 'express';
import { ApolloServer, gql } from 'apollo-server-express';
import { Server } from 'socket.io';
import { createServer } from 'http';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.NODE_ENV === 'production' ? false : ['http://localhost:5500', 'http://127.0.0.1:5500'],
  },
});

// Serve static files (e.g., HTML, CSS, and JS)
app.use(express.static('public'));

// GraphQL schema
const typeDefs = gql`
  type Query {
    messages: [String]
  }

  type Mutation {
    addMessage(message: String): [String]
  }

  type Subscription {
    messageAdded: String
  }
`;

const messages = [];

const resolvers = {
  Query: {
    messages: () => messages,
  },
  Mutation: {
    addMessage: (_, { message }) => {
      messages.push(message);
      io.emit('messageAdded', `${message}`);
      return messages;
    },
  },
  Subscription: {
    messageAdded: {
      subscribe: () => io.asyncIterator(['messageAdded']),
    },
  },
};

const apolloServer = new ApolloServer({
  typeDefs,
  resolvers,
});

async function startApolloServer() {
  await apolloServer.start();
  apolloServer.applyMiddleware({ app });
}

startApolloServer();

const PORT = process.env.PORT || 3500;

httpServer.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}${apolloServer.graphqlPath}`);
});

io.on('connection', (socket) => {
  console.log(`User ${socket.id} connected`);

  socket.on('message', (data) => {
    console.log(data);
    io.emit('messageAdded', `${socket.id.substring(0, 5)}: ${data}`);
  });
});
