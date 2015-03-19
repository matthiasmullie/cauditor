// visualizations/Abstract.js must be loaded before this file

Codegraphs.Visualization.Treemap = Codegraphs.Visualization.Treemap || {};

Codegraphs.Visualization.Treemap.Abstract = function() {
    Codegraphs.Visualization.Abstract.call(this, arguments);
};
Codegraphs.Visualization.Treemap.Abstract.prototype = Object.create(Codegraphs.Visualization.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.data = function(data) {
    return data;
};

/**
 * d3plus visualization.
 *
 * @return {d3plus.viz}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.visualization = function() {
    return d3plus.viz()
        .type('tree_map')
        // nesting package > class
        .id(this.id)
        // set column to calculate size of blocks for
        // don't group really small blocks into an 'other' block
        .size({ 'threshold' : false, 'value': this.size })
        // show full depth (0 = package level; 1 = class)
        .depth(this.id.length)
        // color blocks from green to red, based on a particular column & range
        .color(function(d) {
            var value = this.color[0],
                range = this.color[1],
                color = d3.scale.linear()
                    .domain(range)
                    // green - yellow - red
                    .range(['#006600', '#EECC00', '#EE6600']);

            /*
             * value can be:
             * * column name for value in d
             * * callback function, accepting d, returning value
             */
            value = typeof(value) === 'function' ? value(d) : d[value];
            return color(value)
        }.bind(this))
        // don't show a legend of the colors; that'd be pretty useless since
        // our weighed value isn't the actual value anymore
        .legend(false)
        // d3plus capitalizes (and lowercases rest of the string) by default; I
        // want the text to display as-is
        .format({ 'text': function(text, key) {
            return text;
        } })
        // title of tooltip = fully qualified class name
        .text(['fqcn'])
        // values to be displayed in tooltip; don't show share % or children
        .tooltip({ 'value': this.tooltip, 'share': false, 'children': false })
        // don't show any labels; fqcn are too long for those tiny blocks
        .labels(false)
        // can't zoom in, everything's shown on class-level already
        .zoom(false);
};

/**
 * Id to use for d3plus.viz().id()
 *
 * @type {string[]}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.id = ['name'];

/**
 * Column to base blocks' size on (d3plus.viz().size())
 *
 * @type {string[]}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.size = 'loc';

/**
 * Column to color blocks by, and green-yellow-red thresholds.
 *
 * @type {{string: number[]}}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.color = ['loc', [0, 10, 100]];

/**
 * Array of columns to include in tooltip
 *
 * @type {string[]}
 */
Codegraphs.Visualization.Treemap.Abstract.prototype.tooltip = [];
