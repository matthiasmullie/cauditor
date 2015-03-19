// main.js must be loaded before this file

Codegraphs.Visualization = Codegraphs.Visualization || {};

Codegraphs.Visualization.Abstract = function() {
    // constructor
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Codegraphs.Visualization.Abstract.prototype.nodes = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
Codegraphs.Visualization.Abstract.prototype.visualization = function() {
    return d3plus.viz();
};
