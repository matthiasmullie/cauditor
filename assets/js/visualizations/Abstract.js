// ../QualityControl.js must be loaded before this file

QualityControl.Visualization = QualityControl.Visualization || {};

QualityControl.Visualization.Abstract = function() {
    // constructor
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
QualityControl.Visualization.Abstract.prototype.filter = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
QualityControl.Visualization.Abstract.prototype.visualization = function() {
    return d3plus.viz();
};
