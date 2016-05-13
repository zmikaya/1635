Meteor.methods({
    // 'startBackend': function() {
    //     let client = new Zerorpc();
    //     client.connect('')
    // }
    
    'setThrottle': function(playerID, throttle) {
        Aircraft.update({'_id': playerID}, {$set: {'throttle': throttle}});
    },
    
    'setPitch': function(playerID, pitch) {
        Aircraft.update({'_id': playerID}, {$set: {'pitch': pitch}});
    },
    
    'setRoll': function(playerID, roll) {
        Aircraft.upsert({'_id': playerID}, {$set: {'roll': roll}});
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
    
    'stopSystem': function(playerID) {
        Aircraft.update({'_id': playerID},
            {$set: {'halt': 1}}
        );
    },
    
    'startSystem': function(playerID) {
        // Make sure the system was actually stopped.
        Meteor.call('stopSystem', playerID);
        Aircraft.update({'_id': playerID},
            {$set: {'halt': 0}}
        );
        
        // let client = new Zerorpc()
        // client.connect("tcp://0.0.0.0:4242");
        // client.invoke('startSimulator', 'filler', function(error, res) {
        //     console.log(error);
        // });
    },
    
    'addPlayer': function() {
        
        let playerObj = {
            'x-pos': 300,
            'y-pos': 300,
            'z-pos': 300,
            'pitch': 0,
            'roll': 0,
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