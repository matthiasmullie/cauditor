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
Cauditor.Visualization.Lineplot.Abstract.prototype.visualization = function(metric, range, basis) {
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
                return 'Commit: ' + this.point.commit + '<br>' +
                    'Date: ' + this.point.date + '<br>' +
                    'Average: ' + this.point.avg + '<br>' +
                    'Total: ' + this.point.total + '<br>';
            }
        },
        series: [{
            data: this.transform(this.data, metric, basis),
            animation: false,
            color: '#79b31b'
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
Cauditor.Visualization.Lineplot.Abstract.prototype.transform = function(data, metric, basis) {
    var result = [], point, avg;
    // extract data for this specific metric
    for (var i in data) {
        if (basis === 'method') {
            avg = Math.round(data[i][metric] / Math.max(data[i].nom, 1) * 100) / 100;
        } else if (basis === 'class') {
            avg = Math.round(data[i][metric] / Math.max(data[i].noc, 1) * 100) / 100;
        }

        point = {
            x: parseInt(i),
            y: avg,
            commit: data[i].hash,
            date: data[i].date,
            avg: avg,
            total: data[i][metric]
        };

        result.push(point);
    }

    return result;
};
