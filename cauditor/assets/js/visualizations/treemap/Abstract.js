// visualizations/Abstract.js must be loaded before this file

Cauditor.Visualization.Treemap = Cauditor.Visualization.Treemap || {};

/**
 * @param {Cauditor.Data} data
 */
Cauditor.Visualization.Treemap.Abstract = function(data) {
    Cauditor.Visualization.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Treemap.Abstract.prototype = Object.create(Cauditor.Visualization.Abstract.prototype);

/**
 * highcharts visualization.
 *
 * @see http://api.highcharts.com/highcharts#plotOptions.treemap
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @param {bool} labels Whether or not to show class labels
 * @return {object}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.visualization = function(metric, range, labels) {
    // show class labels by default
    labels = labels !== undefined ? labels : true;

    return {
        colorAxis: {
            min: Math.min(range[0], range[2]),
            max: Math.max(range[0], range[2]),
            stops: this.colors(range)
        },
        legend: {
            // get legend out of here!
            // I could do `enabled: false` instead, but that then seems to affect colors...
            x: 999999,
            y: 999999
        },
        title: {
            enabled: false,
            text: false
        },
        tooltip: {
            // tooltip shows "name: value" by default, but `value` (used for treemap sizing)
            // is LOC; instead, I want the metric (used for colors) to show
            formatter: function () {
                if (this.point.metric === undefined) {
                    // don't show if data is invalid (e.g. when hovering class name)
                    return false;
                }

                return this.point.id + ":" + this.point.metric;
            }
        },
        series: [{
            type: 'treemap',
            layoutAlgorithm: 'squarified',
            data: this.transform(this.data, metric),
            animation: false,
            levels: [{
                // namespace level
                level: 1,
                dataLabels: {
                    enabled: false
                },
                borderWidth: 3,
                borderColor: '#fff'
            }, {
                // class level
                level: 2,
                dataLabels: {
                    enabled: labels,
                    style: {
                        color: '#000'
                    }
                },
                borderWidth: 1,
                borderColor: '#fff'
            }, {
                // method level
                level: 3,
                dataLabels: {
                    enabled: false
                },
                borderWidth: 1,
                borderColor: '#888'
            }],
            alternateStartingDirection: true
        }]
    };
};

/**
 * Returns a data point's FQCN.
 *
 * @param {object} data
 * @param {int} depth
 * @return {string}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.fqcn = function(data, depth) {
    var fqcn = '';

    if (depth === 0) {
        // "project"
        return '';
    } else if (depth === 1) {
        // namespace
        fqcn = data.name;
    } else if (depth === 2) {
        // class
        fqcn = data.parent + '\\' + data.name;
    } else { // if (depth === 3)
        // method
        fqcn = data.parent + '::' + data.name;
    }

    return fqcn.replace(/^\+global\\?/, '');
};

/**
 * Transforms data to the format understood by highcharts.
 * This is not done in `filter`, because the result of that function is kept in memory,
 * to be reused across multiple metrics charts.
 * But we need to narrow it down even further and provide metrics-specific array of data.
 *
 * @param {object} data
 * @param {string} metric
 * @return {object}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.transform = function(data, metric) {
    var result = [], point;
    // extract data for this specific metric
    for (var i in data) {
        point = {
            id: data[i].fqcn,
            name: data[i].name,
            parent: data[i].parent,
            value: data[i].loc,
            metric: data[i][metric],
            colorValue: data[i][metric]
        };

        /*
         * Overriding value.
         * Due to how instability is calculated (ce / (ce + ca)) it's pretty
         * likely to light up red for small classes that have no ca and little
         * ce. Instead of coloring based on the real instability value, I'll
         * change the equation and add 1 to the divisor. For classes without ca,
         * this can drop them significantly if they had little ce; if they have
         * lots of ce and/or ca already, the effect will be minimal.
         * The result of this operation will be that classes with a lot of
         * coupling + instability will light up more than those with lots of
         * instability due to no (or very little) ce.
         */
        if (metric === 'i') {
            point.colorValue = data[i].ce / (data[i].ce + data[i].ca + 3);
        }

        result.push(point);
    }

    return result;
};
