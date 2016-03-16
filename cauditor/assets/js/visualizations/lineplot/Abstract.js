// visualizations/Abstract.js must be loaded before this file

Cauditor.Visualization.Lineplot = Cauditor.Visualization.Lineplot || {};

/**
 * @param {Cauditor.Data} data
 */
Cauditor.Visualization.Lineplot.Abstract = function(data) {
    Cauditor.Visualization.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Lineplot.Abstract.prototype = Object.create(Cauditor.Visualization.Abstract.prototype);

/**
 * highcharts visualization.
 *
 * @see http://api.highcharts.com/highcharts#plotOptions.line
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Abstract.prototype.visualization = function(metric, range) {
    var data = this.transform(this.data, metric);

    return {
        legend: {
            enabled: false
        },
        title: {
            enabled: false,
            text: false
        },
        xAxis: {
            labels: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            formatter: function () {
                date = new Date(this.point.date);
                return 'Commit: ' + this.point.commit + '<br>' +
                    'Date: ' + this.point.date + '<br>' +
                    'Average: ' + this.point.avg + '<br>' +
                    'Worst: ' + this.point.worst + '<br>';
            }
        },
        series: [{
            data: data.avg,
            animation: false,
            turboThreshold: 0,
            color: '#79b31b'
        }, {
            data: data.worst,
            animation: false,
            turboThreshold: 0,
            color: '#f45800'
        }]
    };
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
Cauditor.Visualization.Lineplot.Abstract.prototype.transform = function(data, metric) {
    var result = {avg: [], worst: []}, point, avg;

    // extract data for this specific metric
    for (var i in data) {
        avg = {
            x: parseInt(i),
            y: data[i]['avg_' + metric],
            commit: data[i].hash,
            date: data[i].timestamp,
            avg: data[i]['avg_' + metric],
            worst: data[i]['worst_' + metric]
        };

        worst = {
            x: parseInt(i),
            y: data[i]['worst_' + metric],
            commit: data[i].hash,
            date: data[i].timestamp,
            avg: data[i]['avg_' + metric],
            worst: data[i]['worst_' + metric]
        };

        result.avg.push(avg);
        result.worst.push(worst);
    }

    return result;
};
