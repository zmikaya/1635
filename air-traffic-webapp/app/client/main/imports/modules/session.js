let session = {};

session.closingWindow = function(template) {
    let playerID = template.playerID.get();
    if (playerID !== null) {
        Meteor.call('removePlayer', playerID);
    }
};

session.addPlayer = function(template) {
    let playerID = template.playerID;
    if (playerID.get() == null) {
        Meteor.call('addPlayer', function(error, res) {
            playerID.set(res);
            console.log(playerID.get());
        });
    }
};

export default session;