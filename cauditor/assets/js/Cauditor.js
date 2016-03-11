// vendor/highcharts/highcharts.js must be loaded before this file

/**
 * @param {Cauditor.Visualization.Abstract} visualization
 */
var Cauditor = function(visualization) {
    this.visualization = visualization;
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {array} args Arguments to pass to to visualization.visualization
 */
Cauditor.prototype.draw = function(selector, args) {
    var config = this.visualization.visualization.apply(this.visualization, args);
    $(selector).highcharts(config);
};
