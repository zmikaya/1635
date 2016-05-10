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


/* Initialize state variables */
Template.mainGraphics.onCreated(function() {
	Meteor.call('stopSystem');
	this.rollState = new ReactiveVar(0);
	this.pitchState = new ReactiveVar(0);
	this.boxObjects = new ReactiveVar([]);
	this.aircraftSelection = new ReactiveVar('c130');
});

/* Handle keyboard, mouse, or other peripheral user interactions */
Template.mainGraphics.onRendered(function() {
  let template = this;
  let controlValKeys = Object.keys(controlVals);
  $(window).on('keydown', function(e){
    if (controlValKeys.indexOf(String(e.which)) !== -1) {
      let methodName = controlVals[e.which];
      modules.aircraftControls[methodName](template);
      console.log(template.pitchState.get());
    }
  });
});

Template.mainGraphics.events({
	'click #tie': function(event, template) {
		template.aircraftSelection.set('tie');
	},
	
	'click #c130': function(event, template) {
		template.aircraftSelection.set('c130');
	}
});

Template.mainGraphics.onRendered(function() {
  let template = this;
  
  // Set initial aircraft position
  Meteor.call('setInitialAircraftPos', [300, 300, 300]);
  
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
		// let objSource = './threejs/objects/us-c-130-hercules-airplane-threejs/us-c-130-hercules-airplane.json';
		// let objName = 'c130';
		
		let objSource = './threejs/objects/star-wars-vader-tie-fighter.json';
		let objName = 'tie';
		loader.load(objSource, function(obj) {
			obj.name = objName;
			if (objName == 'tie') {
				obj.scale.set(6, 6, 6);
			}
		  scene.add(obj);
		  obj.position.set(300, 300, 300);
		  aircraft.push(obj);
		  setCameraTarget(obj, 'aircraft');
		  // Create boxes
			let boxes = modules.objects.create(template, [obj.position.x, obj.position.y, obj.position.z]); 
			for (let i=0; i<boxes.length; i++) {
				scene.add(boxes[i]);			
			}
			animate();
		});
		
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
    // if (scene.children) {
    // 	modules.objects.switchAircraft(template, scene, camera, aircraft);
    // }
    

	  var deltaT = clock.getDelta(),
	  time = clock.getElapsedTime() * 10;

    modules.aircraftControls.dynamicsMain(template, aircraft, deltaT);
    modules.objects.controlDynamics(template, aircraft[0], deltaT);

		for ( var i = 0, l = geometry.vertices.length; i < l; i ++ ) {

			geometry.vertices[ i ].y = 35 * Math.sin( i / 5 + ( time + i ) / 7 );

		}

		mesh.geometry.verticesNeedUpdate = true;
  
    camera.update();
		renderer.render( scene, camera );

	}
});