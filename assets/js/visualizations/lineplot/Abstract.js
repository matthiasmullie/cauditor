// visualizations/Abstract.js must be loaded before this file

Caudit.Visualization.Lineplot = Caudit.Visualization.Lineplot || {};

/**
 * @param {Caudit.Data} data
 */
Caudit.Visualization.Lineplot.Abstract = function(data) {
    this.bounds = [];
    Caudit.Visualization.Abstract.apply(this, arguments);

    this.config = {
        type: 'line',
        id: 'stub',
        color: function() {
            return '#fc7e3f';
        },
        x: 'date',
        y: 'score',
        aggs: { 'score': 'mean' },
        time: { 'value': 'date' },
        format: {
            'number': function(number, key) {
                return Math.round(number * 10000) / 10000;
            }
        }
    };
};
Caudit.Visualization.Lineplot.Abstract.prototype = Object.create(Caudit.Visualization.Abstract.prototype);

/**
 * d3plus visualization.
 *
 * @param {string|callback} value Name of the metric column
 * @return {d3plus.viz}
 */
Caudit.Visualization.Lineplot.Abstract.prototype.visualization = function(value) {
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
Caudit.Visualization.Abstract.prototype.filter = function(data) {
    var total = data.length,
        outliers = Math.round(data.length * 0.05),
        result = [];

    if (data.length === 0) {
        return [];
    }

    // gather metrics (= all keys except for 'date')
    metrics = {};
    for (metric in data[0]) {
        if (metric === 'date') {
            continue;
        }
        metrics[metric] = metric;
    }

    // remove commits with 0 on all metrics; likely non-code related
    // commits that shouldn't influence the results
    for (i in data) {
        empty = true;
        for (metric in metrics) {
            if (data[i][metric] !== 0) {
                empty = false;
                break;
            }
        }

        if (empty) {
            delete data[i];
        }
    }

    // split up per metric
    for (metric in metrics) {
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

        // remove % outliers on both sides
        result[metric] = result[metric].slice(outliers, -outliers);
    }

    return result;
};
