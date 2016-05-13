/* global THREE */

import noUiSlider from '../../../imports/js/nouislider.min';
import wNumb from '../../../imports/js/wNumb';

import Aircraft from '../../../../lib/collections/aircraft';


let aircraftControls = {};

/* Create the throttle slider object */
aircraftControls.createThrottleSlider = function(template, document) {
  template.throttleSlider = new ReactiveVar(document.getElementById('slider-vertical'));
  noUiSlider.create(template.throttleSlider.get(), {
  	start: 0,
  	step: 1,
  	orientation: 'vertical',
  	connect: 'lower',
  	direction: 'rtl',
  	tooltips: [wNumb({ decimals: 0 })],
  	range: {
  		'min': 0,
  		'max': 10
  	},
  	pips: {
  	  mode: 'steps',
  	 // density: 5
  	}
  });
};

/* Increment the aircraft throttle */
aircraftControls.throttleUp = function(template) {
  let throttleSlider = template.throttleSlider.get();
  let throttleState = Math.round(Number(throttleSlider.noUiSlider.get()));
  if (throttleState < 10) {
    throttleSlider.noUiSlider.set(throttleState + 1);
    let playerID = template.playerID.get();
    Meteor.call('setThrottle', playerID, throttleState + 1);
  }
  
};

/* Decrement the aircraft throttle */
aircraftControls.throttleDown = function(template) {
  let throttleSlider = template.throttleSlider.get();
  let throttleState = Math.round(Number(throttleSlider.noUiSlider.get()));
  if (throttleState > 0) {
    throttleSlider.noUiSlider.set(throttleState - 1);
    let playerID = template.playerID.get();
    Meteor.call('setThrottle', playerID, throttleState - 1);
  }
};

/* Roll aircraft toward the left */
aircraftControls.rollLeft = function(template) {
  let rollState = template.rollState;
  let rollStateVal = rollState.get();
  if (rollStateVal > -Math.PI/2) {
    rollState.set(rollStateVal - (Math.PI/2)/5);
    let playerID = template.playerID.get();
    Meteor.call('setRoll', playerID, rollState.get());
  }
};

/* Roll aircraft toward the right */
aircraftControls.rollRight = function(template) {
  let rollState = template.rollState;
  let rollStateVal = rollState.get();
  if (rollStateVal < Math.PI/2) {
    rollState.set(rollStateVal + (Math.PI/2)/5);
    let playerID = template.playerID.get();
    Meteor.call('setRoll', playerID, rollState.get());
  }
};

/* Pitch aircraft up */
aircraftControls.pitchUp = function(template) {
  let pitchState = template.pitchState;
  let pitchStateVal = pitchState.get();
  if (pitchStateVal < Math.PI/2) {
    pitchState.set(pitchStateVal + (Math.PI/2)/5);
    let playerID = template.playerID.get();
    Meteor.call('setPitch', playerID, pitchState.get());
  }
};

/* Pitch aircraft down */
aircraftControls.pitchDown = function(template) {
  let pitchState = template.pitchState;
  let pitchStateVal = pitchState.get();
  if (pitchStateVal > -Math.PI/2) {
    pitchState.set(pitchStateVal - (Math.PI/2)/5);
    let playerID = template.playerID.get();
    Meteor.call('setPitch', playerID, pitchState.get());
  }
};

aircraftControls._resetOrientation = function(template) {
  let playerID = template.playerID.get();
  template.rollState.set(0);
  Meteor.call('setRoll', template.rollState.get());
  template.pitchState.set(0);
  Meteor.call('setPitch', playerID, template.pitchState.get());
};

aircraftControls.startSystem = function(template) {
  this._resetOrientation(template);
  let playerID = template.playerID.get();
  Meteor.call('startSystem', playerID);
};

aircraftControls.stopSystem = function(template) {
  let playerID = template.playerID.get();
  Meteor.call('stopSystem', playerID);
};

/* This is the main function that runs any private functions that involve
   the aircraft's primary dynamics.
*/
aircraftControls.dynamicsMain = function(template, aircraft, deltaT) {
  this._updatePosition(template, aircraft, deltaT);
};

aircraftControls._updatePosition = function(template, aircraft, deltaT) {
  // let throttleSlider = template.throttleSlider.get();
  // let throttleState = Math.round(Number(throttleSlider.noUiSlider.get()));
  // let speed = throttleState*40;
  // let distance = speed * deltaT;
  // for (let i=0; i<aircraft.length; i++) {
  //   aircraft[i].position.z += distance;
  //   console.log(aircraft[i].position.z);
  // }
  let playerID = template.playerID.get();
  let aircraft_pos = Aircraft.findOne({_id: playerID});
  let x_pos = aircraft_pos['x-pos'];
  let y_pos = aircraft_pos['y-pos'];
  let z_pos = aircraft_pos['z-pos'];
  
  let rollStateVal = template.rollState.get();
  let pitchStateVal = template.pitchState.get();
  
  for (let i=0; i<aircraft.length; i++) {
    let obj = aircraft[i];
    obj.position.x = z_pos;
    obj.position.y = y_pos;
    obj.position.z = x_pos;
    obj.rotation.x = pitchStateVal;
    obj.rotation.z = rollStateVal;
    // console.log(Math.abs(x_pos) + 300);
  }
  
};

export default aircraftControls;