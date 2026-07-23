import asyncio
import json
import websockets

async def main():
    async with websockets.connect('ws://127.0.0.1:8000/ws/crisis-room') as ws:
        await ws.send(json.dumps({'action': 'start_negotiation', 'scenario_id': 'hurricane_port_2024'}))
        for _ in range(4):
            msg = await ws.recv()
            print(msg)

asyncio.run(main())
