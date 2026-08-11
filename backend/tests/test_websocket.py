import asyncio
import json
import pytest
import websockets

async def run_ws_client_check():
    """Manual helper to test live WebSocket connection to local server."""
    try:
        async with websockets.connect('ws://127.0.0.1:8000/ws/crisis-room') as ws:
            await ws.send(json.dumps({'action': 'ping'}))
            msg = await ws.recv()
            data = json.loads(msg)
            return data.get("type") == "pong"
    except Exception:
        return False

if __name__ == "__main__":
    success = asyncio.run(run_ws_client_check())
    print(f"WebSocket Ping Test Success: {success}")
