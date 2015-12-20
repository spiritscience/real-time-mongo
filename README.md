# real-time-mongo
A set of wrappers for mongodb that allow real-time data output streams, and
links them to a websocket server

You will find that each method within these files are explained in detail
using comments. If you want to know how a method works, take a look at where
it is defined in the source.

## Installation
The requirements for this project are:
- Python >= 3.3
- pip install websockets
- pip install asyncio
- pip install flask
- a working installation of mongodb
- an installed webserver that allows the use of wsgi

I've been working with apache mod_wsgi, but instructions for deploying to
other platforms (eg. nGinX) can be found
[here](http://flask.pocoo.org/docs/0.10/deploying/).

### Instructions for Apache
1. You need to install apache mod_wsgi, on debian based systems:
`sudo apt-get install libapache2-mod-wsgi`

2. Restart Apache. `sudo sevice apache2 restart`

3. Configure you wsgi file. I've included a template. You need to point it to
the location of this directory, so that apache knows where to find all the
libraries in this directory.

4. Assuming you already have a virtualhost setup, add lines to your apache
config file (Probably in `/etc/apache2/apache.conf`, or
`/etc/apache2/sites-enabled/000-default.conf`) until it looks something like
this:

```xml
<VirtualHost *>
    ...
    ...
    # add a wsgi application
    WSGIDaemonProcess real-time-mongo user=user1 group=group1 threads=5
    # add an alias for the wsgi file
    WSGIScriptAlias /api /path/to/this/repo/yourWsgiFile.wsgi

    # create a virtual directory
    <Directory /path/to/this/repo>
        # link this directoy to our wsgi application
        WSGIProcessGroup real-time-mongo
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>

```

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
