// visualizations/Abstract.js must be loaded before this file

QualityControl.Visualization.Lineplot = QualityControl.Visualization.Lineplot || {};

/**
 * @param {QualityControl.Data} data
 */
QualityControl.Visualization.Lineplot.Abstract = function(data) {
    this.bounds = [];
    QualityControl.Visualization.Abstract.apply(this, arguments);

    this.config = {
        type: 'line',
        id: 'stub',
        x: 'date',
        y: 'score',
        aggs: { 'score': 'mean' },
        time: { 'value': 'date' },
        title: { 'total': { 'prefix': 'Average change: ' } },
        format: {
            'number': function(number, key) {
                return Math.round(number * 10000) / 10000;
            }
        }
    };
};
QualityControl.Visualization.Lineplot.Abstract.prototype = Object.create(QualityControl.Visualization.Abstract.prototype);

/**
 * d3plus visualization.
 *
 * @param {string|callback} value Name of the metric column
 * @return {d3plus.viz}
 */
QualityControl.Visualization.Lineplot.Abstract.prototype.visualization = function(value) {
    return d3plus.viz()
        .data(this.data[value])
        .config(this.config);
};

/**
 * Transforms the data & removes the % outliers for all metrics.
 *
 * @param {object} data
 * @return {object}
 */
QualityControl.Visualization.Abstract.prototype.filter = function(data) {
    var total = data.length,
        five = Math.round(data.length * 0.01),
        result = [];

    if (data.length === 0) {
        return [];
    }

    // split up per metric
    for (metric in data[0]) {
        if (metric === 'date') {
            continue;
        }

        result[metric] = [];
        for (i in data) {
            result[metric].push({
                'date': data[i]['date'],
                'score': data[i][metric],
                'stub': '' // need some non-unique value for .id()
            });
        }
    }

    for (metric in result) {
        // sort based on metric score
        result[metric].sort(function(a, b) {
            return a.score > b.score ? 1 : -1;
        });

        // remove 5% outliers on both sides
        result[metric] = result[metric].slice(five, -five);
    }

    return result;
};
