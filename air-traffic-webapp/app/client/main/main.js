/* global THREE */
/* global $ */

import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import Detector from '../imports/js/Detector';
import Stats from '../imports/js/stats.min';

import controlVals from './imports/utils/controlVals';
import modules from './imports/modules/mainModules';

import Aircraft from '../../lib/collections/aircraft';

import './main.html';

/* Handle keyboard, mouse, or other peripheral user interactions */
Template.mainGraphics.onRendered(function() {
  let template = this;
  let controlValKeys = Object.keys(controlVals);
  $(window).on('keydown', function(e){
    if (controlValKeys.indexOf(String(e.which)) !== -1) {
      let methodName = controlVals[e.which];
      modules.aircraftControls[methodName](template);
    }
  });
});

Template.mainGraphics.onRendered(function() {
  let template = this;
  modules.aircraftControls.createThrottleSlider(template, document);


  if ( ! Detector.webgl ) {

		Detector.addGetWebGLMessage();
		document.getElementById( 'container' ).innerHTML = "";

	}

	var container, stats;

	var camera, controls, scene, renderer;

	var mesh, texture, geometry, material;

	var worldWidth = 128, worldDepth = 128,
	worldHalfWidth = worldWidth / 2, worldHalfDepth = worldDepth / 2;

	var clock = new THREE.Clock();
	
	var aircraft = [];

	init();
	animate();

	function init() {

		container = document.getElementById( 'container' );

		// camera = new THREE.PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 1, 20000 );
		// camera.position.y = 200;
		camera = new THREE.TargetCamera(60, window.innerWidth / window.innerHeight, 1, 20000);

		// controls = new THREE.FirstPersonControls( camera );

		// controls.movementSpeed = 500;
		// controls.lookSpeed = 0.1;

		scene = new THREE.Scene();
		scene.fog = new THREE.FogExp2( 0xaaccff, 0.0007 );

		geometry = new THREE.PlaneGeometry( 20000, 20000, worldWidth - 1, worldDepth - 1 );
		geometry.rotateX( - Math.PI / 2 );

		for ( var i = 0, l = geometry.vertices.length; i < l; i ++ ) {

			geometry.vertices[ i ].y = 35 * Math.sin( i / 2 );

		}

		texture = new THREE.TextureLoader().load( "./threejs/textures/water.jpg" );
		texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
		texture.repeat.set( 5, 5 );

		material = new THREE.MeshBasicMaterial( { color: 0x0044ff, map: texture } );

		mesh = new THREE.Mesh( geometry, material );
		scene.add( mesh );
		
		// Load aircraft
		var loader = new THREE.ObjectLoader();
		loader.load('./threejs/objects/us-c-130-hercules-airplane-threejs/us-c-130-hercules-airplane.json', function(obj) {
		  scene.add(obj);
		  obj.position.set(300, 300, 300);
		  aircraft.push(obj);
		  setCameraTarget(obj, 'aircraft');
		});
		
		function setCameraTarget(obj, name) {
		  // Set the camera target using the THREE.TargetCamera lib
		  camera.addTarget({
        name: name,
        targetObject: obj,
        cameraPosition: new THREE.Vector3(0, 10, 50),
        fixed: false,
        stiffness: 0.1,
        cameraRotation: new THREE.Euler(0, Math.PI, 0),
        matchRotation: true
      });
      camera.setTarget('aircraft');
		}

		renderer = new THREE.WebGLRenderer();
		renderer.setClearColor( 0xaaccff );
		renderer.setPixelRatio( window.devicePixelRatio );
		renderer.setSize( window.innerWidth, window.innerHeight );

		container.innerHTML = "";

		container.appendChild( renderer.domElement );

		stats = new Stats();
		container.appendChild( stats.dom );

		//

		window.addEventListener( 'resize', onWindowResize, false );

	}

	function onWindowResize() {

		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();

		renderer.setSize( window.innerWidth, window.innerHeight );

	}

	//

	function animate() {

		requestAnimationFrame( animate );
		render();
		stats.update();

	}

	function render() {
    // let x_pos = Aircraft.findOne({'name': 'b2'})['x-pos']
    // console.log(x_pos);
    
	  var deltaT = clock.getDelta(),
	  time = clock.getElapsedTime() * 10;

    modules.aircraftControls.dynamicsMain(template, aircraft, deltaT);

		for ( var i = 0, l = geometry.vertices.length; i < l; i ++ ) {

			geometry.vertices[ i ].y = 35 * Math.sin( i / 5 + ( time + i ) / 7 );

		}

		mesh.geometry.verticesNeedUpdate = true;
  
    camera.update();
		renderer.render( scene, camera );

	}
});