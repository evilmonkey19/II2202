const url = "ws://localhost:3549/myWebsocket"
const mywsServer = new WebSocket(url)

const myMessages = document.getElementById("messages")
const myInput = document.getElementById("message")
const sendBtn = document.getElementById("send")


sendBtn.disabled = true
sendBtn.addEventListener("click", sendMsg, false)

function sendMsg() {
    const text = myInput.value
    myInput.value = ""
    msgGeneration(text, "Client")
    mywsServer.send(text)
}

function msgGeneration(msg, from) {
    const newMessage = document.createElement("li")
    newMessage.innerText = `${from} says: ${msg}`
    myMessages.appendChild(newMessage)
}

mywsServer.onopen = function() {
    sendBtn.disabled = false
}

mywsServer.onmessage = function(event) {
    const { data } = event
    msgGeneration(data, "Server")
}