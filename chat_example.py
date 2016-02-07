import RTM
import time

# runs for each message sent by each client
def handler(websocket):
    recv = yield from websocket.recv()
    if recv[:8] == 'LISTEN: ':
        data = recv[8:]
        try:
            req = json.loads(data)
        except:
            yield from websocket.send("Invalid request: Not JSON")
            return False
        # check we have all the values we need
        if not "recipient_pairs" in req or not 'collection' in req \
                or not 'sender_pair' in req:
            yield from websocket.send("Invalid request: Wrong params")
            return False
        # recipients info
        recipient_pairs = req['recipient_pairs']
        # sender info
        sender_pair = req['sender_pair']
        # collection is the name of the collection
        collection = req['collection']
        # find the documents addressed to any of the recipients
        mongo = RTM.MongoConnection()
        stream = mongo.message_stream(
            sender_pair,
            recipient_pairs,
            collection
        )
        if not stream:
            yield from websocket.send("Invalid request: Invalid recipient")
            return False
        # this for loop bocks, so nothing after it will be executed.
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

# instantiate a websocket server
wss = RTM.WSServer(debug=True)
# add our threads to the websocket server
wss.add_send_thread(handler)

# start the websocket server. This method never returns
wss.start()
