Meteor.methods({
    // 'startBackend': function() {
    //     let client = new Zerorpc();
    //     client.connect('')
    // }
    
    'setThrottle': function(throttle) {
        Aircraft.upsert({'name': 'b2'}, {$set: {'throttle': throttle}});
    }
})