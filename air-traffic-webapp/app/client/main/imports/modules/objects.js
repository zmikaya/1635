/* global THREE */
/* global Aircraft */
/* global _ */

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
        if (distance > 20) {
            this._update(boxObjects[i], aircraftPos);
        }
        if (boxObject.position.y < 150) {
            this._update(boxObjects[i], aircraftPos);
        }
    }
};

objects._makeFall = function(template, deltaT) {
    let boxObjects = template.boxObjects.get();
    for (let i=0; i<boxObjects.length; i++) {
        boxObjects[i].position.y -= 100*deltaT;
    }
};

objects.controlDynamics = function(template, aircraft, deltaT) {
    let playerID = template.playerID.get();
    let halt = Aircraft.findOne({_id: playerID}).halt;
    // if (!halt) {
        let aircraftPos = [aircraft.position.x, aircraft.position.y, aircraft.position.z];
        this._checkPositions(template, aircraftPos);
        this._makeFall(template, deltaT);
    // }
};

objects.switchAircraft = function(template, scene, camera, aircraft) {
    let aircraftTypes = ['c130', 'tie'];
    let aircraftSelection = template.aircraftSelection.get();
    console.log(scene.getObjectByName(aircraftSelection));
    if (!(scene.getObjectByName(aircraftSelection))) {
        for (let i=0; i<aircraftTypes.length; i++) {
            let currentAircraft = scene.getObjectByName(aircraftTypes[i]);
            if (currentAircraft) {
                scene.remove(currentAircraft);
                break;
            }
            if (i==aircraftTypes.length) {
                return;
            }
        }
        let objSource;
        if (aircraftSelection == 'c130') {
            objSource = './threejs/objects/us-c-130-hercules-airplane-threejs/us-c-130-hercules-airplane.json';
        }
        else if (aircraftSelection == 'tie') {
            objSource = './threejs/objects/star-wars-vader-tie-fighter.json';
        }
        var loader = new THREE.ObjectLoader();
		loader.load(objSource, function(obj) {
		  obj.name = aircraftSelection;
		  scene.add(obj);
		  obj.position.set(300, 300, 300);
		  obj.scale(4, 4, 4);
		  aircraft
		  aircraft.push(obj);
		  function setCameraTarget(obj, name) {
		  // Set the camera target using the THREE.TargetCamera lib
        		camera.addTarget({
                name: name,
                targetObject: obj,
                cameraPosition: new THREE.Vector3(0, 10, 50),
                fixed: false,
                stiffness: 0.05,
                cameraRotation: new THREE.Euler(0, Math.PI, 0),
                matchRotation: true
            });
            camera.setTarget('aircraft');
            }
    		setCameraTarget(obj, 'aircraft');
		});
    }
}

objects.createOtherAircraft = function() {
    let playerIDS = Aircraft.find({}, {fields:{_id: 1}}).fetch();
    playerIDS = _.pluck(playerIDS, '_id');
    for (let i=0; i<playerIDS.length; i++) {
        if (!(scene.getObjectByName(playerIDS[i]))) {
            var loader = new THREE.ObjectLoader();
    		let objSource = './threejs/objects/us-c-130-hercules-airplane-threejs/us-c-130-hercules-airplane.json';
    		let objName = 'c130';
    		
    		// let objSource = './threejs/objects/star-wars-vader-tie-fighter.json';
    		// let objName = 'tie';
    		loader.load(objSource, function(obj) {
    		obj.name = objName;
    		if (objName == 'tie') {
    			obj.scale.set(6, 6, 6);
    		}
    		obj.name = playerIDS[i];
    	    scene.add(obj);
    	    let aircraft = Aircraft.findOne({_id: playerIDS[i]});
    	    let x_pos = aircraft['x-pos'];
    	    let y_pos = aircraft['y-pos'];
    	    let z_pos = aircraft['z-pos'];
    	    obj.position.set(z_pos, y_pos, x_pos);
            });
        }
    }
};

export default objects;