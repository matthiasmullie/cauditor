// ../Cauditor.js must be loaded before this file

Cauditor.Visualization = Cauditor.Visualization || {};

/**
 * @param {Cauditor.Data} data
 */
Cauditor.Visualization.Abstract = function(data) {
    this.data = data.filter(this.filter);
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Abstract.prototype.filter = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
Cauditor.Visualization.Abstract.prototype.visualization = function() {
    return d3plus.viz();
};
