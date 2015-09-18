// visualizations/Abstract.js must be loaded before this file

Caudit.Visualization.Treemap = Caudit.Visualization.Treemap || {};

/**
 * @param {Caudit.Data} data
 */
Caudit.Visualization.Treemap.Abstract = function(data) {
    Caudit.Visualization.Abstract.apply(this, arguments);
    this.config = {
        type: 'tree_map',
        data: this.data,
        // nesting package > class
        id: this.id,
        // set column to calculate size of blocks for
        // don't group really small blocks into an 'other' block
        size: { 'threshold' : false, 'value': this.size },
        // show full depth (0 = package level; 1 = class)
        depth: this.id.length,
        // don't show a legend of the colors; that'd be pretty useless since
        // our weighed value isn't the actual value anymore
        legend: false,
        // title of tooltip = fully qualified class name
        text: ['fqcn'],
        // don't show any labels; fqcn are too long for those tiny blocks
        labels: false,
        // can't zoom in, everything's shown on class-level already
        zoom: false
    };
};
Caudit.Visualization.Treemap.Abstract.prototype = Object.create(Caudit.Visualization.Abstract.prototype);

/**
 * d3plus visualization.
 *
 * @param {string|callback} value Name of the column holding value to color by, or callback function
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @param {object} tooltip Object in { columnname: text } format
 * @return {d3plus.viz}
 */
Caudit.Visualization.Treemap.Abstract.prototype.visualization = function(value, range, tooltip) {
    tooltip = tooltip || this.tooltip;

    return d3plus.viz()
        .config(this.config)
        // d3plus capitalizes (and lowercases rest of the string) by default; I
        // want the text to display as-is
        .format({
            'text': function(tooltip, text, key) {
                // check if full text was defined for tooltip
                if (text in tooltip) {
                    return tooltip[text];
                }

                return text;
            }.bind(this, tooltip)
        })
        // values to be displayed in tooltip; don't show share % or children
        .tooltip({ 'value': Object.keys(tooltip), 'share': false, 'children': false })
        // color blocks from green to red, based on a particular column & range
        .color(function(value, range, d) {
            var color = d3.scale.linear()
                .domain(range)
                // green - yellow - red
                .range(['#1F9B1F', '#F4BE00', '#F45800']);

            /*
             * value can be:
             * * column name for value in d
             * * callback function, accepting d, returning value
             */
            value = typeof(value) === 'function' ? value(d) : d[value];
            return color(value)
        }.bind(this, value, range));
};

/**
 * Id to use for d3plus.viz().id()
 *
 * @type {string[]}
 */
Caudit.Visualization.Treemap.Abstract.prototype.id = ['name'];

/**
 * Column to base blocks' size on (d3plus.viz().size())
 *
 * @type {string[]}
 */
Caudit.Visualization.Treemap.Abstract.prototype.size = 'loc';

/**
 * Array of columns to include in tooltip
 *
 * @type {Object} Object in { columnname: text } format
 */
Caudit.Visualization.Treemap.Abstract.prototype.tooltip = { 'loc': 'Lines of code' };
