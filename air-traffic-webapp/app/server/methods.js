Meteor.methods({
    // 'startBackend': function() {
    //     let client = new Zerorpc();
    //     client.connect('')
    // }
    
    'setThrottle': function(throttle) {
        Aircraft.upsert({'name': 'b2'}, {$set: {'throttle': throttle}});
    },
    
    'setPitch': function(pitch) {
        Aircraft.upsert({'name': 'b2'}, {$set: {'pitch': pitch}});
    },
    
    'setRoll': function(roll) {
        Aircraft.upsert({'name': 'b2'}, {$set: {'roll': roll}});
    },
    
    'setInitialAircraftPos': function(pos) {
        Aircraft.upsert({'name': 'b2'}, 
        {$set: {'x-pos': pos[0], 
                'y-pos': pos[1], 
                'z-pos': pos[2],
                'pitch': pos[3],
                'roll': pos[4]
        }});
    }
})