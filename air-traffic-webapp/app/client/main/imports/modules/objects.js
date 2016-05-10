/* global THREE */
/* global Aircraft */

let objects = {};

objects._getRandomArbitrary = function(min, max) {
  return Math.random() * (max - min) + min;
};

objects.create = function(template, aircraftPos) {
    let boxObjects = template.boxObjects.get();
    
    let boxGeometry = new THREE.BoxBufferGeometry( 20, 20, 20 );
	
    while (boxObjects.length < 50) {
        let boxObj = new THREE.Mesh( boxGeometry, new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } ) );
        let x = this._getRandomArbitrary(aircraftPos[0]-300, aircraftPos[0]+300);
        let y = this._getRandomArbitrary(aircraftPos[0]+100, aircraftPos[0]+250);
        let z = this._getRandomArbitrary(aircraftPos[2]-300, aircraftPos[2]+300);
        console.log(x);
        boxObj.position.set(x, y, z);
        boxObjects.push(boxObj);
    }
    template.boxObjects.set(boxObjects);
    return boxObjects;
};

objects._update = function(boxObj, aircraftPos) {
    let x = this._getRandomArbitrary(aircraftPos[0]-300, aircraftPos[0]+300);
    let y = this._getRandomArbitrary(aircraftPos[0]+100, aircraftPos[0]+250);
    let z = this._getRandomArbitrary(aircraftPos[2]-300, aircraftPos[2]+300);
    boxObj.position.set(x, y, z);
};

objects._checkPositions = function(template, aircraftPos) {
    let boxObjects = template.boxObjects.get();
    for (let i=0; i<boxObjects.length; i++) {
        let boxObject = boxObjects[i];
        let x_dist = Math.pow((boxObject.x-aircraftPos[0]), 2);
        let y_dist = Math.pow((boxObject.y-aircraftPos[1]), 2);
        let z_dist = Math.pow((boxObject.z-aircraftPos[2]), 2);
        let distance = Math.sqrt(x_dist + y_dist + z_dist);
        if (distance > 50) {
            this._update(boxObjects[i], aircraftPos);
        }
        console.log(boxObject.position.y);
        if (boxObject.position.y < 150) {
            this._update(boxObjects[i], aircraftPos);
        }
    }
};

objects._makeFall = function(template, deltaT) {
    let boxObjects = template.boxObjects.get();
    for (let i=0; i<boxObjects.length; i++) {
        boxObjects[i].position.y -= 80*deltaT;
    }
};

objects.controlDynamics = function(template, aircraft, deltaT) {
    let halt = Aircraft.findOne({'name': 'b2'}).halt;
    if (!halt) {
        let aircraftPos = [aircraft.position.x, aircraft.position.y, aircraft.position.z];
        this._checkPositions(template, aircraftPos);
        this._makeFall(template, deltaT);
    }
};

export default objects;