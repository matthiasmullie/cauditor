// ../Cauditor.js must be loaded before this file

Cauditor.Visualization = Cauditor.Visualization || {};

/**
 * @param {Cauditor.Data} data
 */
Cauditor.Visualization.Abstract = function(data) {
    this.data = data.filter(this);
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
 * highcharts config.
 *
 * @return {object}
 */
Cauditor.Visualization.Abstract.prototype.visualization = function() {
    return {};
};
