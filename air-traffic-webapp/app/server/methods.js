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
    },
    
    'stopSystem': function() {
        Aircraft.upsert({'name': 'b2'},
            {$set: {'halt': 1}}
        );
    },
    
    'startSystem': function() {
        // Make sure the system was actually stopped.
        Meteor.call('stopSystem');
        Aircraft.upsert({'name': 'b2'},
            {$set: {'halt': 0}}
        );
        
        let client = new Zerorpc()
        client.connect("tcp://0.0.0.0:4242");
        client.invoke('startSimulator', 'filler', function(error, res) {
            console.log(error);
        });
    },
    
    'addPlayer': function() {
        
        let playerObj = {
            'x-pos': 300,
            'y-pos': 300,
            'z-pos': 300,
            'pitch': null,
            'roll': null,
            'throttle': 0,
            'halt': 1
        };
        
        let _id = Aircraft.insert(playerObj);
        
        return _id;
        
    },
    
    'removePlayer': function(playerID) {
        Aircraft.remove({_id: playerID});
        console.log('removed');
    }
})