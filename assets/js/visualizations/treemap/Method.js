// visualizations/treemap/Abstract.js must be loaded before this file

Codecharts.Visualization.Treemap.Method = function() {
    Codecharts.Visualization.Treemap.Abstract.call(this, arguments);
};
Codecharts.Visualization.Treemap.Method.prototype = Object.create(Codecharts.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Codecharts.Visualization.Treemap.Method.prototype.data = function(data) {
    return d3.layout.treemap().nodes(data).filter(function(d) {
        // if there's a children node, we're not on method-level
        if (d.children !== undefined) {
            return false;
        }

        d.package = d.parent.parent.name;
        d.class = d.parent.name;

        d.fqcn = d.class + '::' + d.name;
        if (d.package !== '+global') {
            d.fqcn = d.package + '\\' + d.fqcn;
        }

        return true;
    });
};

Codecharts.Visualization.Treemap.Method.prototype.id = ['package', 'class', 'name'];
Codecharts.Visualization.Treemap.Method.prototype.tooltip = ['loc', 'ccn', 'npath'];
