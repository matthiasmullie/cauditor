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
    var result = [], avg, worst;

    // sort on date: oldest first
    data.sort(function(a, b) {
        return a.timestamp > b.timestamp ? 1 : -1;
    });

    for (i in data) {
        data[i].count = parseInt(i);

        avg = Object.create(data[i]);
        avg.id = 'avg';
        avg.color = '#1F9B1F'; // green
        result.push(avg);

        worst = Object.create(data[i]);
        worst.id = 'worst';
        worst.color = '#F45800'; // red
        result.push(worst);
    }

    return result;
};

/**
 * Text "translations" to use for d3plus.viz().format()
 *
 * @type {string{}}
 */
Cauditor.Visualization.Lineplot.Progress.prototype.format = {
    'timestamp': 'Date',
    'avg_mi': 'Average',
    'avg_ccn': 'Average',
    'avg_npath': 'Average',
    'avg_i': 'Average',
    'avg_ca': 'Average',
    'avg_ce': 'Average',
    'worst_mi': 'Worst',
    'worst_ccn': 'Worst',
    'worst_npath': 'Worst',
    'worst_i': 'Worst',
    'worst_ca': 'Worst',
    'worst_ce': 'Worst'
};
