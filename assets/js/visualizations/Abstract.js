// ../Caudit.js must be loaded before this file

Caudit.Visualization = Caudit.Visualization || {};

/**
 * @param {Caudit.Data} data
 */
Caudit.Visualization.Abstract = function(data) {
    this.data = data.filter(this.filter);
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Caudit.Visualization.Abstract.prototype.filter = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
Caudit.Visualization.Abstract.prototype.visualization = function() {
    return d3plus.viz();
};
