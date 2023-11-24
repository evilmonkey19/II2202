import WebSocket, { WebSocketServer } from 'ws'
import express from "express"
import path from "path"
import { fileURLToPath } from 'url'
import fs from 'fs'

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

let messages = []
wsServer.on("connection", function connection(ws) {
    ws.on('error', console.error);

    ws.on('message', function message(data) {
        wsServer.clients.forEach(function each(client) {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
        if (data.toString() === 'close') {
            ws.close();
            process.emit('SIGINT');
            return;
        }
        messages.push(`${data},${new Date().toISOString()}`);
    });
})

httpServer.on('upgrade', async function upgrade(request, socket, head) {
    wsServer.handleUpgrade(request, socket, head, function done(ws) {
        wsServer.emit('conection', ws, request);
    });
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
    console.log("Closing server, come tomorrow!")
    const csvContent = messages.join('\n');
    const fileName = getNextFileName('../results/websockets/servers', 'server', 'csv');
    fs.writeFileSync(fileName, csvContent);
    process.exit();
});

// https://dev.to/codesphere/getting-started-with-web-sockets-in-nodejs-49n0