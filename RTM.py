import pymongo
import util
import time

class RTM:
    util = util.Util()

    # Stores information in the specified collection
    def store(self, data, collection, visible=False):
        collection = self.util.db[collection]
        # Note: If the user stores data with key='visible', it will be
        # overwritten here for security reasons.
        # Note: Documents with visible=True can be read by the front end
        # which includes the user! So no password hashes. No sensitive info
        # unless it's their own.
        data['visible'] = visible
        collection.insert(data)

    # Creates a generator or stream for a given query on a given collection
    def stream(self, query, collection):
        stream = self.util.db[collection].find(
            query,
            cursor_type=pymongo.cursor.CursorType.TAILABLE
        )
        return stream if stream else False

    
    ### This section of the library is for generating documents that can   ###
    ### only be read by the desired recipient, using networking, not       ###
    ### cryptography. Note: A recipient is not limited to a person, and    ###
    ### may also be, say, a channel, room, or group. Anything that         ###
    ### represents something that has access to documents that not         ###
    ### _everyone_ should have access to.                                  ###
    
    # Adds a recipient (returns that recipient's ID)
    def add_recipient(self, pub, password):
        # don't create duplicate users
        if self.util.db.recipients.find_one({"pub": pub.lower()}):
            return False
        return self.util.db.recipients.insert({
            "pub": pub.lower(),
            "priv": self.util.sha512(password)
        })

    # Adds data to a collection, but so that only the recipients can recieve
    # it using the recieve_stream method
    def send(self, data, sender_pair, recipient, collection):
        # authenticate the sender
        sender_key = self.util.sha512(sender_pair[1])
        sender = self.util.db.recipients.find_one(
            {"pub": sender_pair[0], "priv": sender_key}
        )
        if not sender: return False
        # die if the sender was not found
        if not sender: return False
        # store the message
        return self.store(
            {
                "data": data,
                "sender": sender_pair[0],
                "recipient": recipient,
                "ts": time.time()
            },
            collection,
            visible=True
        )

    # Grabs a stream for messages directed to a list of recipients
    # To call this method, you must be the sender, and all of the recipients.
    # This is so that nobody can request messages that they are not cleared to
    # see. Note: By "being the recipients", that could either mean that you
    # were the individual recipient, or that you were the a member of that
    # channel or group etc.
    def receive_stream(self, sender_pair, recipient_pairs, collection):
        # convert passwords into private keys
        recipient_pubs = []
        recipient_privs = []
        for pair in recipient_pairs:
            recipient_pubs.append(pair[0])
            recipient_privs.append(self.util.sha512(pair[1]))
        sender_pub = sender_pair[0]
        sender_priv = self.util.sha512(sender_pair[1])
        recipient_collection = self.util.db.recipients
        recipients = []
        # validate creds
        for recipient_pair, recipient in zip(recipient_pairs,
                recipient_collection.find({
                    "$and": [
                        {"priv": {"$in": recipient_privs}},
                        {"pub": {"$in": recipient_pubs}}
                    ]
                })):
            # the above will return all users with the same priv, so we need
            # to narrow it down. Note: The above query could be streamlined
            if recipient['pub'] == recipient_pair[0] \
                    and recipient['priv'] == recipient_pair[1]:
                recipients.append(recipient['pub'])
        sender = recipient_collection.find_one(
            {"pub": sender_pub, "priv": sender_priv}
        )
        if not sender: return False
        sender = sender['pub']
        # return a stream of messages directed towards the keys specified
        return self.stream(
            {
                "$or": [
                    {'recipient': {"$in": recipients}},
                    {'sender': sender}
                ]
            },
            collection
        )

