// vendor/d3.min.js & vendor/d3plus.min.js must be loaded before this file

/**
 * @param {QualityControl.Data} data
 * @param {QualityControl.Visualization.Abstract} visualization
 */
var QualityControl = function(data, visualization) {
    this.data = data;
    this.visualization = visualization;
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {array} args Arguments to pass to to visualization.visualization
 */
QualityControl.prototype.draw = function(selector, args) {
    var data = this.data.filter(this.visualization.filter);
    this.visualization.visualization.apply(this.visualization, args)
        .container(selector)
        .data(data)
        .draw();
};
