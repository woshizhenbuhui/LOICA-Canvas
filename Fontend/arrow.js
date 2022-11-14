/**
 * Using the mouse to draw arrows
 */

(function(window, document) {
	if (window.mapleque == undefined)
		window.mapleque = {};
	if (window.mapleque.arrow != undefined)
		return;

	/**
	 * External interface to components
	 */
	var proc = {
		/**
		 * Receive a canvas object and draw an arrow on it
		 * @param context
		 */
		paint: function(context) {
			paint(this, context);
		},
		/**
		 * Set arrow start and end points
		 * @param sp Starting point
		 * @param ep Ending point
		 * @param st Intensity
		 */
		set: function(sp, ep, st) {
			init(this, sp, ep, st);
		},
		/**
		 * Set arrow appearance
		 * @param args
		 */
		setPara: function(args) {
			this.size = args.arrow_size; //arrow size
			this.sharp = args.arrow_sharp;
		}
	};

	var init = function(a, sp, ep, st) {
		a.sp = sp;
		a.ep = ep;
		a.st = st;
	};
	var paint = function(a, context) {
		var sp = a.sp;
		var ep = a.ep;
		if (context == undefined)
			return;
		//Draw arrow main line
		context.beginPath();
		context.moveTo(sp.x, sp.y);
		context.lineTo(ep.x, ep.y);
		//Draw arrow head
		var h = _calcH(a, sp, ep, context);
		context.moveTo(ep.x, ep.y);
		context.lineTo(h.h1.x, h.h1.y);
		context.moveTo(ep.x, ep.y);
		context.lineTo(h.h2.x, h.h2.y);
		context.stroke();
	};
	// Calculate head coordinates
	var _calcH = function(a, sp, ep, context) {
		var theta = Math.atan((ep.x - sp.x) / (ep.y - sp.y));
		var cep = _scrollXOY(ep, -theta);
		var csp = _scrollXOY(sp, -theta);
		var ch1 = {
			x: 0,
			y: 0
		};
		var ch2 = {
			x: 0,
			y: 0
		};
		var l = cep.y - csp.y;
		ch1.x = cep.x + l * (a.sharp || 0.025);
		ch1.y = cep.y - l * (a.size || 0.05);
		ch2.x = cep.x - l * (a.sharp || 0.025);
		ch2.y = cep.y - l * (a.size || 0.05);
		var h1 = _scrollXOY(ch1, theta);
		var h2 = _scrollXOY(ch2, theta);
		return {
			h1: h1,
			h2: h2
		};
	};
	//spin coordinates
	var _scrollXOY = function(p, theta) {
		return {
			x: p.x * Math.cos(theta) + p.y * Math.sin(theta),
			y: p.y * Math.cos(theta) - p.x * Math.sin(theta)
		};
	};

	var arrow = new Function();
	arrow.prototype = proc;
	window.mapleque.arrow = arrow;
})(window, document);
