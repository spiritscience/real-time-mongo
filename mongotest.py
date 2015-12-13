#!/usr/bin/env python3

import pymongo
import json
import re
import time

# Read config
config = json.load(open('config.json', 'r'))
# Connect to MongoDB
client = pymongo.MongoClient(config['mongo_host'], config['mongo_port'])
db = client["test"]
collection = db['messages']

messages = collection.find({}, cursor_type=34)
#messages = collection.find({})
while messages.alive:
    for message in messages:
        #message = messages.next()
        print(message)
