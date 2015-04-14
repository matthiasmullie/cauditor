// vendor/d3.min.js & vendor/d3plus.min.js must be loaded before this file

var QualityControl = function(path) {
    var that = this;
    d3.json(path, function(data) {
        that.data = data;
    });
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {QualityControl.Visualization.Abstract} visualization
 */
QualityControl.prototype.draw = function(selector, visualization) {
    if (this.data === undefined) {
        setTimeout(this.draw.bind(this, selector, visualization), 50);
        return;
    }

    var data = visualization.data(this.data);

    visualization.visualization()
        .container(selector)
        .data(data)
        .draw();
};
