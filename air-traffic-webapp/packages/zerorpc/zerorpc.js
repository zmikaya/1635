let Future = Npm.require("fibers/future");
let zerorpc = Npm.require('zerorpc');

// Zerorpc = {
//     client: undefined,
//     connect: function (tcp) {
//         this.client = new zerorpc.Client();
//         this.client.connect(tcp);
//         this.client.on("error", function (error) {
//             console.error("RPC client error: ", error);
//         });
//     },
//     invoke: function (method, kwargs) {
//         if (this.client) {
//             var fut = new Future();

//             this.client.invoke(method, kwargs, function (error, res, more) {
//                 if (error) {
//                     console.error(error);
//                     fut['return']([]);
//                 } else {
//                     console.log(res);
//                     fut['return'](res);
//                 }
//                 if (!more) {
//                     console.log('zerorpc.invoke('+method+')Done!');
//                 }
//             });

//             return fut.wait();

//         } else {
//             console.error("connect the zerorpc server first, then invoke method here!! ");
//         }

//     }
// };

class ZerorpcClass {
    constructor(timeout=5, heartbeatInterval=5000) {
        let options = {
            'timeout': timeout,
            'heartbeatInterval': heartbeatInterval
        };
        this.client = new zerorpc.Client(options);
    }

    connect(tcp_address) {
        this.client.connect(tcp_address);
        this.client.on("error", error => {
            console.error(`RPC client error: ${error}`);
        });
        // `return this` to help with `method chaining`
        return this;
    }

    invoke(method, kwargs) {
        if (this.client) {
            let fut = new Future();
            console.warn(`ZerorpcClass.invoke(${method}, ${JSON.stringify(kwargs)}) -> Start to RUN!`);
            this.client.invoke(method, kwargs, (error, result, more) => {
                if (error) {
                    console.error(`ZerorpcClass.invoke(${method}, ${JSON.stringify(kwargs)}) -> Error! - ${error}`);
                    // fut.return(error);
                    fut.throw(error);
                } else {
                    console.log(`zerorpc.invoke(${method}) | ` +
                                `kwargs -> ${JSON.stringify(kwargs)} -> Done!`);
                    fut.return(result);
                }
                if (!more) {
                    console.log(`zerorpc.invoke(${method}) | ` +
                                `kwargs -> ${JSON.stringify(kwargs)} -> ...!`)
                }
            });
            return fut.wait();
            // return fut;
        } else {
            console.error("`connect` the zerorpc server first, " +
                          "then `invoke` method here!! ");
        }
    }
}

Zerorpc = ZerorpcClass;