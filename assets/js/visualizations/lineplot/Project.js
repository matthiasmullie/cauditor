// visualizations/lineplot/Abstract.js must be loaded before this file

Cauditor.Visualization.Lineplot.Project = function() {
    Cauditor.Visualization.Lineplot.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Lineplot.Project.prototype = Object.create(Cauditor.Visualization.Lineplot.Abstract.prototype);

/**
 * d3plus config.
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Project.prototype.visualization = function(metric, range) {
    var config = Cauditor.Visualization.Lineplot.Abstract.prototype.visualization.apply(this, arguments);

    return $.extend(config, {
        x: {
            value: 'x',
            grid: false,
            label: false
        },
        y: function(data, key) {
            // with a value of 0, the chart fails to render
            return data[data.id] || .00001;
        },
        // values to be displayed in tooltip; don't show share % or children etc
        tooltip: {
            size: false,
            value: ['timestamp', 'weighed', 'worst'],
            // whatever size is required to fit the text in
            small: '100%'
        },
        // color blocks from green to red, based on a particular column & range
        color: 'color'
    });
};

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Project.prototype.filter = function(data) {
    var result = [], weighed, worst;

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

        weighed = Object.create(data[i]);
        weighed.id = 'weighed';
        weighed.color = '#1F9B1F'; // green
        result.push(weighed);

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
Cauditor.Visualization.Lineplot.Project.prototype.format = {
    'timestamp': 'Date',
    'weighed': 'Average',
    'worst': 'Worst',
};
