// visualizations/lineplot/Abstract.js must be loaded before this file

Cauditor.Visualization.Lineplot.Progress = function() {
    Cauditor.Visualization.Lineplot.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Lineplot.Progress.prototype = Object.create(Cauditor.Visualization.Lineplot.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Progress.prototype.filter = function(data) {
    // sort on date: oldest first
    data.sort(function(a, b) {
        return a.date > b.date ? 1 : -1;
    });

    return data;
};
