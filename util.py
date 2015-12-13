import pymongo
import json
import hashlib

class Util:
    def __init__(self):
        # Read config
        self.config = json.load(open('config.json', 'r'))
        # Connect to MongoDB
        self.mongo = pymongo.MongoClient(self.config['mongo_host'], self.config['mongo_port'])
        self.db = self.mongo[self.config['mongo_database']]

    # Shorthand for sha512 sum
    def sha512(self, string):
        return hashlib.sha512(string.encode('utf-8')).hexdigest()
