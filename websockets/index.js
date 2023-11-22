import { WebSocketServer } from 'ws'
import express from "express"
import path from "path"
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const PORT = process.env.PORT || 3500

const app = express()

app.use(express.static(path.join(__dirname, "public")))

const httpServer = app.listen(PORT, () => {
    console.log(`listening on port ${PORT}`)
    console.log(`Connect to http://localhost:${PORT}`)
})

const wsServer = new WebSocketServer({ port: 3549 });

wsServer.on("connection", function connection(ws) {
    ws.on('error', console.error);

    ws.on('message', function message(data) {
        console.log(`received: ${data} : ${new Date().toISOString()}`);
    });
})

httpServer.on('upgrade', async function upgrade(request, socket, head) {
    wsServer.handleUpgrade(request, socket, head, function done(ws) {
        wsServer.emit('conection', ws, request);
    });
});

// https://dev.to/codesphere/getting-started-with-web-sockets-in-nodejs-49n0