// visualizations/treemap/Abstract.js must be loaded before this file

Cauditor.Visualization.Treemap.Method = function() {
    Cauditor.Visualization.Treemap.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Treemap.Method.prototype = Object.create(Cauditor.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Treemap.Method.prototype.filter = function(data) {
    var fqcn = [];
    return d3.layout.treemap().nodes(data).filter(function(d) {
        // CCN metric is only on method-level (also project-wide sum, which is excluded by the d.name check)
        if (d.ccn === undefined || d.name === undefined) {
            return false;
        }

        d.package = d.parent.parent.name;
        d.class = d.parent.name;

        d.fqcn = d.class + '::' + d.name;
        if (d.package !== '+global') {
            d.fqcn = d.package + '\\' + d.fqcn;
        }

        // skip duplicates
        if (fqcn.indexOf(d.fqcn) >= 0) {
            return false;
        }
        fqcn.push(d.fqcn);

        return true;
    });
};

Cauditor.Visualization.Treemap.Method.prototype.id = ['package', 'class', 'name'];