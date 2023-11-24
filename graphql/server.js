import { execute, subscribe } from "graphql"
import { ApolloServer, gql } from "apollo-server-express"
import { PubSub } from "graphql-subscriptions"
import { SubscriptionServer } from "subscriptions-transport-ws"
import { makeExecutableSchema } from "@graphql-tools/schema"

import { createServer } from "http"

import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'

// General
const app = express();
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const PORT = process.env.PORT || 3501;


// GraphQL
const httpServer = createServer(app);
const pubsub = new PubSub();

const typeDefs = gql`    
type Query {
  viewMessages: [Message!]
}
type Mutation {
  sendMessage(name: String, content: String): Message!
}
type Subscription {
  receiveMessage: Message!
}
type Message {
   id: ID!
   name: String!
   content: String
}`;
let messages = [];
let close = 0;
const resolvers = {
  Query: {
     viewMessages() {},
  },
  Mutation: {
      sendMessage: (parent, { name, content }) => {
        try{
          const id = messages.length;
          pubsub.publish("MessageService", {receiveMessage:  { id, name, content }});
          close = content === 'close' ? 1 : 0;
          if (!close) {
            messages.push(`${content}, ${new Date().toISOString()}`);
          }
          return { id , name, content };
        } finally {
          if (close) {
            setTimeout(() => {
              process.emit('SIGINT');
            }, 1000);
          }
        }
      },
  },
  Subscription: {
        receiveMessage: {
          subscribe:()=> pubsub.asyncIterator(["MessageService"]),
        },
   },
};

const schema = makeExecutableSchema({ typeDefs, resolvers });
const server = new ApolloServer({schema,});
await server.start();
server.applyMiddleware({ app });
SubscriptionServer.create({ schema, execute, subscribe },{ server: httpServer, path: '/graphql'});


// Serve statics
app.use(express.static(path.join(__dirname, "public")))

// General
httpServer.listen(PORT, () => {
  console.log(`Query endpoint ready at http://localhost:${PORT}${server.graphqlPath}`);
  console.log(`Subscription endpoint ready at ws://localhost:${PORT}${server.graphqlPath}`);
});

function getNextFileName(baseDir, baseName, extension) {
  let counter = 1;
  while (true) {
      const fileName = `${baseDir}/${baseName}_${counter}.${extension}`;
      if (!fs.existsSync(fileName)) {
          return fileName;
      }
      counter++;
  }
}

process.on('SIGINT', function () {
  console.log("Closing server, come tomorrow!");
  const csvContent = messages.join('\n');
  const fileName = getNextFileName('../results/graphql/servers', 'messages', 'csv');
  fs.writeFileSync(fileName, csvContent);
  process.exit();
});