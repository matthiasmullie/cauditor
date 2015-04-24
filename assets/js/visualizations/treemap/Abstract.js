// visualizations/Abstract.js must be loaded before this file

QualityControl.Visualization.Treemap = QualityControl.Visualization.Treemap || {};

/**
 * @param {QualityControl.Data} data
 */
QualityControl.Visualization.Treemap.Abstract = function(data) {
    QualityControl.Visualization.Abstract.apply(this, arguments);
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
        // d3plus capitalizes (and lowercases rest of the string) by default; I
        // want the text to display as-is
        format: { 'text': function(text, key) {
            return text;
        } },
        // title of tooltip = fully qualified class name
        text: ['fqcn'],
        // values to be displayed in tooltip; don't show share % or children
        tooltip: { 'value': this.tooltip, 'share': false, 'children': false },
        // don't show any labels; fqcn are too long for those tiny blocks
        labels: false,
        // can't zoom in, everything's shown on class-level already
        zoom: false
    };
};
QualityControl.Visualization.Treemap.Abstract.prototype = Object.create(QualityControl.Visualization.Abstract.prototype);

/**
 * d3plus visualization.
 *
 * @param {string|callback} value Name of the column holding value to color by, or callback function
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @return {d3plus.viz}
 */
QualityControl.Visualization.Treemap.Abstract.prototype.visualization = function(value, range) {
    return d3plus.viz()
        .config(this.config)
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
QualityControl.Visualization.Treemap.Abstract.prototype.id = ['name'];

/**
 * Column to base blocks' size on (d3plus.viz().size())
 *
 * @type {string[]}
 */
QualityControl.Visualization.Treemap.Abstract.prototype.size = 'loc';

/**
 * Array of columns to include in tooltip
 *
 * @type {string[]}
 */
QualityControl.Visualization.Treemap.Abstract.prototype.tooltip = [];
