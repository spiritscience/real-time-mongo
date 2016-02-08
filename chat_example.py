import RTM
import time
import threading

# runs for each message sent by each client
def listen_handler(websocket, recv):
    if recv[:len("listen: ")].lower() == 'listen: ':
        data = recv[8:]
        try:
            req = json.loads(data)
        except:
            yield from websocket.send("listen: Not JSON")
            return False
        # check we have all the values we need
        if not "recipient_pairs" in req or not 'collection' in req \
                or not 'sender_pair' in req:
            yield from websocket.send("listen: Wrong params")
            return False
        # recipients info
        recipient_pairs = req['recipient_pairs']
        # sender info
        sender_pair = req['sender_pair']
        # collection is the name of the collection
        collection = req['collection']
        # find the documents addressed to any of the recipients
        stream = mongo.message_stream(
            sender_pair,
            recipient_pairs,
            collection
        )
        if not stream:
            yield from websocket.send("listen: Invalid recipient")
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

def send_handler(websocket, recv):
    # if the first part of the line is "Send :"
    if recv[:len("send: ")].lower() == "send: ":
        data = json.loads(recv[len("send: "):])
        if not "sender_pair" in data or not "recipient" in data or not \
                "collection" in data:
            yield from websocket.send("send: Invalid Arguments")
        sender_pair = data['sender_pair']
        recipient = data['recipient']
        collection = "messages"
        
        mongo.send(data, sender_pair, recipient, collection)
        yield from websocket("send: Message sent")

def handler(websocket):
    recv = yield from websocket.recv()
    threading.Thread(target=listen_handler, args=(websocket, recv)).start()
    threading.Thread(target=send_handler, args=(websocket, recv)).start()

# connection to the mongo db
mongo = RTM.MongoConnection()
# instantiate a websocket server
wss = RTM.WSServer(debug=True)
# add our threads to the websocket server
wss.add_handler(handler)

# start the websocket server. This method never returns
wss.start()
