// vendor/d3.min.js & vendor/d3plus.min.js must be loaded before this file

/**
 * @param {QualityControl.Data} data
 */
var QualityControl = function(data) {
    this.data = data;
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {QualityControl.Visualization.Abstract} visualization
 */
QualityControl.prototype.draw = function(selector, visualization) {
    visualization.visualization()
        .container(selector)
        .data(this.data.filter(visualization.filter))
        .draw();
};
