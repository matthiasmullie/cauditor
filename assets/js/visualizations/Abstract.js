// main.js must be loaded before this file

Codecharts.Visualization = Codecharts.Visualization || {};

Codecharts.Visualization.Abstract = function() {
    // constructor
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Codecharts.Visualization.Abstract.prototype.nodes = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
Codecharts.Visualization.Abstract.prototype.visualization = function() {
    return d3plus.viz();
};
