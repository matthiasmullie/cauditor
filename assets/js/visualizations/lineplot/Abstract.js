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
 * d3plus config.
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {object}
 */
Cauditor.Visualization.Lineplot.Abstract.prototype.visualization = function(metric, range) {
    return {
        type: 'line',
        id: 'id',
        // color blocks from green to red, based on a particular column & range
        color: 'color',
        // don't show a legend of the colors
        legend: false,
        // title of tooltip = commit hash
        text: {
            value: function(data, key) {
                return data.hash;
            }
        },
        format: {
            // d3plus capitalizes (and lowercases rest of the string) by default; I
            // want the text to display as-is
            text: function(text, key) {
                // ... or have some translation or alternative text
                if (text in this.format) {
                    return this.format[text];
                }

                return text;
            }.bind(this),
            number: function(number, key) {
                // round to 2 decimals
                return Math.round(number * 10000) / 10000;
            }
        }
    };
};

/**
 * Text "translations" to use for d3plus.viz().format()
 *
 * @type {string{}}
 */
Cauditor.Visualization.Lineplot.Abstract.prototype.format = {};
