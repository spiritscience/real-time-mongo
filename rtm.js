function RTM(url){
    this.url = url;

    // Open a socket listening for database changes
    this.listen = function(collection, sender_pair, recipient_pairs, callback){
        var callback = callback || false;   // make callback optional
        // Connect to socketserver
        var ws = new WebSocket(this.url);
        // set the response callback
        ws.onmessage = function(data){
            // run the callback
            if (callback) {
                callback(data);
            }
            // trigger the event
            $(this).trigger('eachDocument');
        };
        query = {
            collection: collection,
            sender_pair: sender_pair,
            recipient_pairs: recipient_pairs
        };
        ws.onopen = function(){
            ws.send('LISTEN: ' + JSON.stringify(query));
        }
    }
    
}
