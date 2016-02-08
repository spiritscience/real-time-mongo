function RTM(url){
    this.url = url;
    // Connect to socketserver
    this.ws = new WebSocket(this.url);
    this.handlers = [];

    // define the message callback
    this.message_callback = function(message){
        // iterate the handlers
        for (var i in this.handlers){
            handler = this.handlers[i];
            // run the handlers
            handler(message);
        }
        $(this).trigger('eachDocument');
    }
    // set the message callback
    this.ws.onmessage = this.message_callback;

    // Tells the server to listen for database changes and send them to us
    this.listen = function(collection, sender_pair, recipient_pairs, callback){
        var callback = callback || false;   // make callback optional
        // set the response callback
        var handler = function(data){
            // run the callback
            if (callback) {
                callback(data);
            }
            // trigger the event
        };
        this.handlers.push(handler)
        query = {
            collection: collection,
            sender_pair: sender_pair,
            recipient_pairs: recipient_pairs
        };
        ws.send('LISTEN: ' + JSON.stringify(query));
    }
    
    this.send = function(collection, sender_pair, recipient_pairs){
        this.ws.send("SEND: " + JSON.stringify({
            collection: collection,
            sender_pair: sender_pair,
            recipient_pairs: recipient_pairs
        });
    }
}
