// visualizations/treemap/Abstract.js must be loaded before this file

Cauditor.Visualization.Treemap.Method = function() {
    Cauditor.Visualization.Treemap.Abstract.apply(this, arguments);
};
Cauditor.Visualization.Treemap.Method.prototype = Object.create(Cauditor.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @param {int} depth
 * @return {object}
 */
Cauditor.Visualization.Treemap.Method.prototype.filter = function(data, depth) {
    var relevant = [], children = [];
    depth = depth || 0;

    data.fqcn = this.fqcn(data);

    for (var i in data.children) {
        if (depth === 1) {
            // relay package & class name to children
            data.children[i].package = data.name;
        } else if (depth === 2) {
            // relay package & class name to children
            data.children[i].package = data.package;
            data.children[i].class = data.name;
        }

        children = this.filter(data.children[i], depth + 1);
        relevant = relevant.concat(children);
    }

    // CCN metric is only on method-level
    if (data.ccn !== undefined) {
        relevant.push(data);
    }

    return relevant;
};

/**
 * Id to use for d3plus.viz().id()
 *
 * @type {string[]}
 */
Cauditor.Visualization.Treemap.Method.prototype.id = ['package', 'class', 'name'];
