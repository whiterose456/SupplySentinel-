class ConnectionManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket):
        self.connections.append(websocket)

    async def disconnect(self, websocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)
