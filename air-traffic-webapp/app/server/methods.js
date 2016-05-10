Meteor.methods({
    // 'startBackend': function() {
    //     let client = new Zerorpc();
    //     client.connect('')
    // }
    
    'setThrottle': function(throttle) {
        Aircraft.upsert({'name': 'b2'}, {$set: {'throttle': throttle}});
    },
    
    'setInitialAircraftPos': function(pos) {
        Aircraft.upsert({'name': 'b2'}, 
        {$set: {'x-pos': pos[0], 'y-pos': pos[0], 'z-pos': pos[0]}});
    }
})