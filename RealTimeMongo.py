from time import time
from RTM import RTM
from flask import Flask

app = Flask(__name__)
rtm = RTM()

# Sends a message by storing in the database.
@app.route('/send')
def send_message():
    if request.method == "POST":
        data = request.form['data']
        crate = json.loads(data)
        rtm.send(crate, 'messages' visible=True)

@app.route('/')
def index():
    return 'Index Page!'

if __name__ == '__main__':
    app.run(debug=True)
