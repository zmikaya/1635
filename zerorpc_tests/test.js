// var zerorpc = require("zerorpc");

// var server = new zerorpc.Server({
//     hello: function(name, reply) {
//         console.log('val: ' + name);
//         reply(null, 'None');
//     }
// });

// server.bind("tcp://0.0.0.0:4242");

var zerorpc = require("zerorpc");

var server = new zerorpc.Server({
    sendPos: function(pos, reply) {
        console.log('pos: ' + pos);
        reply(null, 'None');
    }
});

server.bind("tcp://0.0.0.0:4242");