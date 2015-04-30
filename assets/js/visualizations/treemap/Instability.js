// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.Instability = function() {
    QualityControl.Visualization.Treemap.Class.apply(this, arguments);
};
QualityControl.Visualization.Treemap.Instability.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

/**
 * d3plus visualization.
 *
 * @param {string|callback} value Name of the column holding value to color by, or callback function
 * @param {array} range Array with 3 values: good, medium & bad threshold values [g, y, r]
 * @param {object} tooltip Object in { columnname: text } format
 * @return {d3plus.viz}
 */
QualityControl.Visualization.Treemap.Instability.prototype.visualization = function(value, range, tooltip) {
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
    var value = function(d) {
        return d.ce / (d.ce + d.ca + 3);
    };
    return QualityControl.Visualization.Treemap.Class.prototype.visualization.call(this, value, range, tooltip);
};
