# real-time-mongo
A set of wrappers for mongodb that allow real-time data output streams, and
links them to a websocket server

## FlaskApi.py
A Flask application that can be called from the front end to perform certain
database functions.

## RTM.py
The central python library that controls this project.

## RealTimeMongo.wsgi
This is an example file that you can point WSGI to in order to add the Flask
API to your webserver.

## config.json
This file contains database information. You can find an example file in
`config.json.template`

## rtm.js
This is the JavaScript wrapper for the websocket server and the Flask API.

## util.py
This library handles and maintains database connections, and also provides
some short-hand functions for simplicity.

## websocket-server.py
This is a websocket server that must be running for this application to work.
It's purpose is to provide a live stream of messages to the front end without
polling and wasting resources. It's the primary advantage of using this system.
