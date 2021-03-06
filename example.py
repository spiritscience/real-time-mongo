import RTM
import asyncio
import time

# Repeats all users messages back to them
# runs for each message sent by each client
def handler(websocket):
    # wait for message
    try:
        recv = yield from websocket.recv()
    except ConnectionClosed as e:
        # the connection died. Do code
        pass
    # send message
    yield from websocket.send(recv)

# instantiate a websocket server
wss = RTM.WSServer(debug=True)
# add our threads to the websocket server
wss.add_handler(handler)

# start the websocket server. This method never returns
wss.start()
