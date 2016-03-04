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
    var relevant = [];

    for (var i in data.children) {
        // relay package name to children
        data.children[i].package = data.name;

        filtered_children = this.filter(data.children[i]);
        relevant = relevant.concat(filtered_children);
    }

    // CA metric is only on class-level (also project-wide sum, which is excluded by the d.name check)
    if (data.ca === undefined || data.name === undefined) {
        return relevant;
    }

    data.fqcn = (data.package !== '+global' ? data.package + '\\' : '') + data.name;
    relevant.push(data);
    return relevant;
};

Cauditor.Visualization.Treemap.Class.prototype.id = ['package', 'name'];
