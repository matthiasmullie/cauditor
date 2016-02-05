// visualizations/treemap/Abstract.js must be loaded before this file

Cauditor.Visualization.Treemap.Class = function() {
    Cauditor.Visualization.Treemap.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Treemap.Class.prototype = Object.create(Cauditor.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
Cauditor.Visualization.Treemap.Class.prototype.filter = function(data) {
    var fqcn = [];
    return d3.layout.treemap().nodes(data).filter(function(d) {
        // CA metric is only on class-level (also project-wide sum, which is excluded by the d.name check)
        if (d.ca === undefined || d.name === undefined) {
            return false;
        }

        d.package = d.parent.name;

        d.fqcn = d.name;
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

Cauditor.Visualization.Treemap.Class.prototype.id = ['package', 'name'];
