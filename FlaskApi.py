from time import time
from RTM import RTM
from flask import Flask

app = Flask(__name__)
rtm = RTM()

# Sends a message by storing in the database.
@app.route('/send')
def send_message():
    if request.method == "POST":
        data = str(request.form['data'])
        sender_pair = request.form['sender_pair']
        recipient = request.form['recipient']
        collection = "messages"
        
        rtm.send(data, sender_pair, recipient, collection)

@app.route('/')
def index():
    return 'Index Page!'

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
