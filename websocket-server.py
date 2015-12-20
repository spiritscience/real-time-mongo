#!/usr/bin/env python3
import asyncio
import websockets
import pymongo
import json
import util
import RTM
import logging

rtm = RTM.RTM()
util = util.Util()
    
@asyncio.coroutine
def handle_client(websocket, path):
    while True:
        recv = yield from websocket.recv()
        print(recv if recv else "close")
        if recv == None:
            break
        if recv[:8] == 'LISTEN: ':
            data = recv[8:]
            try:
                req = json.loads(data)
            except:
                yield from websocket.send("Invalid request: Not JSON")
                continue
            # check we have all the values we need
            if not "recipient_pairs" in data or not 'collection' in data \
                    or not 'sender_pair' in data:
                yield from websocket.send("Invalid request: Wrong params")
                continue
            # recipients info
            recipient_pairs = req['recipient_pairs']
            # sender info
            sender_pair = req['sender_pair']
            # collection is the name of the collection
            collection = req['collection']
            # find the documents addressed to any of the recipients
            stream = rtm.receive_stream(
                sender_pair,
                recipient_pairs,
                collection
            )
            if not stream:
                yield from websocket.send("Invalid request: Invalid recipient")
                continue
            # this for loop bocks, so nothing after it will be executed.
            while 1:
                for message in stream:
                    # each message must be tagged as 'visible'.
                    # This is so we don't accidentally give info to the user
                    if message['visible']:
                        data = {
                            "sender": message['sender'],
                            "recipient": message['recipient'],
                            "message": message['data'],
                            "ts": message['ts']
                        }
                        yield from websocket.send(json.dumps(data))

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

start_server = websockets.serve(
    handle_client,
    util.config['websocket_host'],
    util.config['websocket_port']
)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
