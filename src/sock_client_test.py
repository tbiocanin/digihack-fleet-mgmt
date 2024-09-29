#!/usr/bin/env python

import asyncio
from websockets.sync.client import connect

def hello():
    hello = ["A", "st", "256"]
    with connect("ws://localhost:8765") as websocket:
        websocket.send(hello)
        # websocket.send("Another message")
        message = websocket.recv()
        print(f"Received: {message}")

hello()