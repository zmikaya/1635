import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import './main.html';

// Template.hello.onCreated(function helloOnCreated() {
//   // counter starts at 0
//   this.counter = new ReactiveVar(0);
// });

// Template.hello.helpers({
//   counter() {
//     return Template.instance().counter.get();
//   },
// });

// Template.hello.events({
//   'click button'(event, instance) {
//     // increment the counter when button is clicked
//     instance.counter.set(instance.counter.get() + 1);
//   },
// });

Template.hello.onCreated(function() {
    var scene = new THREE.Scene();
  	var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
  
  	var renderer = new THREE.WebGLRenderer();
  	renderer.setSize( window.innerWidth, window.innerHeight );
  	document.body.appendChild( renderer.domElement );
  
  	var geometry = new THREE.BoxGeometry( 1, 1, 1 );
  	var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
  	var cube = new THREE.Mesh( geometry, material );
  	scene.add( cube );
  
  	camera.position.z = 5;
  
  	var render = function () {
  		requestAnimationFrame( render );
  
  		cube.rotation.x += 0.1;
  		cube.rotation.y += 0.1;
  
  		renderer.render(scene, camera);
  	};
  
  	render();
  }
);
