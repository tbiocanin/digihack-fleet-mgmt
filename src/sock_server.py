#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve
import websockets.exceptions

"""
Simple mock functions. Assuming that the coding from the beacon is as follows:

A/B -> direction
xy -> the following number indicating the ID of the vehicle

A/B -> direction
_st -> identifier that it is a (eg.) bus station
xy -> the following number indicating the ID of the station
"""

def _parse_msg_beacon(message):

    # NOTE : add a timestamp hhmmss
    # NOTE : count passangers internaly
    # NOTE : all of those things write to a csv or a txt as a logger of entries that would be used for profiling
    out_val = {
        "smer": "",
        "linija" : 0
    }

    out_val["smer"] = message[0]  
    out_val["linija"] = int(message[1:])

    return out_val

def _parse_msg_station(message):


    out_val = {
        "smer" : "",
        "broj_stanice" : ""
    }

    out_val[0] = message[0]
    out_val["broj_stanice"] = message[3:]

def parse(message):
    print(message)
    out = None
    if message[1:3] == "st":
        out = _parse_msg_station(message=message)
    else:
        out =_parse_msg_beacon(message=message)

    print(out)
    return out

# main functions
async def echo(websocket):

    try:
        async for message in websocket:
            out_msg = parse(message=message)
            # print(out_msg)
            await websocket.send("OK")
    except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
    finally:
            # Ensure the connection is closed gracefully
            await websocket.close()

async def main():
    async with serve(echo, "192.168.20.24", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())