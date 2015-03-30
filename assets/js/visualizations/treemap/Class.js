// visualizations/treemap/Abstract.js must be loaded before this file

Codecharts.Visualization.Treemap.Class = function() {
    Codecharts.Visualization.Treemap.Abstract.call(this, arguments);
};
Codecharts.Visualization.Treemap.Class.prototype = Object.create(Codecharts.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Codecharts.Visualization.Treemap.Class.prototype.data = function(data) {
    return d3.layout.treemap().nodes(data).filter(function(d) {
        // if there's no CA data, we're not on class-level
        if (d.ca === undefined) {
            return false;
        }

        d.package = d.parent.name;

        d.fqcn = d.name;
        if (d.package !== '+global') {
            d.fqcn = d.package + '\\' + d.fqcn;
        }

        return true;
    });
};

Codecharts.Visualization.Treemap.Class.prototype.id = ['package', 'name'];
Codecharts.Visualization.Treemap.Class.prototype.tooltip = ['loc', 'ca', 'ce', 'i', 'cr', 'wmc', 'dit'];
