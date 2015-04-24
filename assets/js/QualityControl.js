// vendor/d3.min.js & vendor/d3plus.min.js must be loaded before this file

/**
 * @param {QualityControl.Visualization.Abstract} visualization
 */
var QualityControl = function(visualization) {
    this.visualization = visualization;
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {array} args Arguments to pass to to visualization.visualization
 */
QualityControl.prototype.draw = function(selector, args) {
    this.visualization.visualization.apply(this.visualization, args)
        .container(selector)
        .draw();
};
