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
 * d3plus config.
 *
 * @param {string} value Name of the metric column
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {object}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.visualization = function(metric, range) {
    return {
        type: 'tree_map',
        // nesting package > class > method
        id: this.id,
        // set column to calculate size of blocks for
        // don't group really small blocks into an 'other' block
        size: { threshold : false, value: 'loc' },
        // show full depth (0 = package level; 1 = class)
        depth: this.id.length,
        // don't show a legend of the colors; that'd be pretty useless since
        // our weighed value isn't the actual value anymore
        legend: false,
        // don't show any labels; fqcn are too long for those tiny blocks
        labels: false,
        // can't zoom in, everything's shown on deepest level already
        zoom: false,
        // title of tooltip = fully qualified class name
        text: {
            value: function(data, key) {
                return data.fqcn + ': ' + data[metric];
            }
        },
        // values to be displayed in tooltip; don't show share % or children etc
        tooltip: {
            size: false,
            share: false,
            children: false,
            // whatever size is required to fit the text in
            small: '100%'
        },
        // d3plus capitalizes (and lowercases rest of the string) by default; I
        // want the text to display as-is
        format: {
            text: function(text, key) {
                return text;
            }
        },
        // color blocks from green to red, based on a particular column & range
        color: function(metric, range, data) {
            var color = d3.scale.linear()
                .domain(range)
                // green - yellow - red
                .range(['#1F9B1F', '#F4BE00', '#F45800']);

            value = data[metric];

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
                value = data.ce / (data.ce + data.ca + 3);
            }

            return color(value);
        }.bind(this, metric, range)
    };
};

/**
 * Returns a data point's FQCN.
 *
 * @param {object} data
 * @return {string}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.fqcn = function(data) {
    var fqcn = '';

    if (data.ccn !== undefined) {
        if (data.class) {
            // method
            fqcn = data.package + '\\' + data.class + '::' + data.name;
        } else {
            // function
            fqcn = data.package + '\\' + data.name;
        }
    } else if (data.ca !== undefined) {
        // class
        fqcn = data.package + '\\' + data.name;
    } else if (data.noc === undefined) {
        // namespace
        fqcn = data.name;
    } else {
        // "project"
        return '';
    }

    return fqcn.replace(/^\+global\\?/, '');
};

/**
 * Id to use for d3plus.viz().id()
 *
 * @type {string[]}
 */
Cauditor.Visualization.Treemap.Abstract.prototype.id = ['name'];
