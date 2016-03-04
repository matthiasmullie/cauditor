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
    var relevant = [];

    for (var i in data.children) {
        // relay package & class name to children
        if (data.package === undefined) {
            data.children[i].package = data.name;
        } else {
            data.children[i].package = data.package;
            data.children[i].class = data.name;
        }

        filtered_children = this.filter(data.children[i]);
        relevant = relevant.concat(filtered_children);
    }

    // CCN metric is only on method-level (also project-wide sum, which is excluded by the d.name check)
    if (data.ccn === undefined || data.name === undefined) {
        return relevant;
    }

    data.fqcn = (data.package !== '+global' ? data.package + '\\' : '') + data.class + data.name;
    relevant.push(data);
    return relevant;
};

Cauditor.Visualization.Treemap.Method.prototype.id = ['package', 'class', 'name'];
