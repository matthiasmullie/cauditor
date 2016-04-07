// visualizations/lineplot/Abstract.js must be loaded before this file

Cauditor.Visualization.Lineplot.User = function() {
    Cauditor.Visualization.Lineplot.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Lineplot.User.prototype = Object.create(Cauditor.Visualization.Lineplot.Abstract.prototype);

/**
 * d3plus config.
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {object}
 */
Cauditor.Visualization.Lineplot.User.prototype.visualization = function(metric, range) {
    var config = Cauditor.Visualization.Lineplot.Abstract.prototype.visualization.apply(this, arguments);

    return $.extend(config, {
        id: 'id',
        x: {
            value: 'x',
            grid: false,
            label: false
        },
        y: function(data, key) {
            // with a value of 0, the chart fails to render
            return data[metric] || .00001;
        },
        // values to be displayed in tooltip; don't show share % or children etc
        tooltip: {
            size: false,
            value: ['timestamp', 'project', metric],
            // whatever size is required to fit the text in
            small: '100%'
        },
        color: function() {
            return '#1F9B1F';
        }
    });
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Lineplot.User.prototype.filter = function(data) {
    // sort on date: oldest first
    data.sort(function(a, b) {
        return a.timestamp > b.timestamp ? 1 : -1;
    });

    for (i in data) {
        // x value must be unique (or data is aggregated), not 0 (or drawing
        // fails), and just a series of increment integers also seems to produce
        // weird charts when there's lots of data...
        // this should do, I guess...
        data[i].x = data[i].timestamp + i;

        data[i].id = '';
    }

    return data;
};

/**
 * Text "translations" to use for d3plus.viz().format()
 *
 * @type {string{}}
 */
Cauditor.Visualization.Lineplot.User.prototype.format = {
    'timestamp': 'Date',
    'project': 'Project',
    'mi': 'Difference',
    'ccn': 'Difference',
    'npath': 'Difference',
    'i': 'Difference',
    'ca': 'Difference',
    'ce': 'Difference'
};
