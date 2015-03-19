// vendor/d3.min.js & vendor/d3plus.min.js must be loaded before this file

var Codegraphs = function(path) {
    this.path = path;
};

/**
 * Draw a new visualization.
 *
 * @param {string} selector
 * @param {Codegraphs.Visualization.Abstract} visualization
 */
Codegraphs.prototype.draw = function(selector, visualization) {
    d3.json(this.path, function(data) {
        data = visualization.data(data);

        visualization.visualization()
            .container(selector)
            .data(data)
            .draw();
    });
};
