import noUiSlider from '../../../imports/js/nouislider.min';
import wNumb from '../../../imports/js/wNumb'; 


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
  }
};

/* Decrement the aircraft throttle */
aircraftControls.throttleDown = function(template) {
  let throttleSlider = template.throttleSlider.get();
  let throttleState = Math.round(Number(throttleSlider.noUiSlider.get()));
  if (throttleState > 0) {
    throttleSlider.noUiSlider.set(throttleState - 1);
  }
};

/* This is the main function that runs any private functions that involve
   the aircraft's primary dynamics.
*/
aircraftControls.dynamicsMain = function(template, aircraft, deltaT) {
  this._updatePosition(template, aircraft, deltaT);
};

aircraftControls._updatePosition = function(template, aircraft, deltaT) {
  let throttleSlider = template.throttleSlider.get();
  let throttleState = Math.round(Number(throttleSlider.noUiSlider.get()));
  let speed = throttleState*40;
  let distance = speed * deltaT;
  for (let i=0; i<aircraft.length; i++) {
    aircraft[i].position.z += distance;
  }
};

export default aircraftControls;