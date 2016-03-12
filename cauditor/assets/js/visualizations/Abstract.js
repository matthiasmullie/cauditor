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

/**
 * In config, colors always range from good (green) to bad (red)
 * good can sometimes be the highest possible number (e.g. maintenance index)
 * and sometimes smallest (e.g. cyclomatic complexity)
 * this swaps colors & calculates the percentage of where things should start
 * to show up as yellow
 *
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {array}
 */
Cauditor.Visualization.Abstract.prototype.colors = function(range) {
    var middle = (range[1] - Math.min(range[0], range[2])) / Math.abs(range[2] - range[0]);
    if (range[0] < range[2]) {
        return [[0, '#1F9B1F'], [middle, '#F4BE00'], [1, '#F45800']];
    } else {
        return [[0, '#F45800'], [middle, '#F4BE00'], [1, '#1F9B1F']];
    }
};
