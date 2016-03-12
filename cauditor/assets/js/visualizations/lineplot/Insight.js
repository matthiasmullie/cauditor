// visualizations/lineplot/Abstract.js must be loaded before this file

Cauditor.Visualization.Lineplot.Insight = function() {
    Cauditor.Visualization.Lineplot.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Lineplot.Insight.prototype = Object.create(Cauditor.Visualization.Lineplot.Abstract.prototype);

/**
 * Transforms the data & removes the % outliers for all metrics.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Insight.prototype.filter = function(data) {
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
    for (i = 0; i < data.length; i++) {
        empty = true;
        for (metric in metrics) {
            if (data[i][metric] !== 0) {
                empty = false;
                break;
            }
        }

        if (empty) {
            data.splice(i, 1);
            i--;
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
