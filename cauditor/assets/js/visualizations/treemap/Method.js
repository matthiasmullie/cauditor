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

    data.fqcn = this.fqcn(data, depth);

    for (var i in data.children) {
        // relay package & class name to children
        data.children[i].parent = data.fqcn;

        children = this.filter(data.children[i], depth + 1);
        relevant = relevant.concat(children);
    }

    // including topmost parent doesn't make sense; we need to start at namespaces
    if (depth === 0) {
        return relevant;
    }

    // we need to include this element because it's parent of nodes that are relevant
    if (children.length > 0) {
        relevant.push(data);
        return relevant;
    }

    // CCN metric is only on method-level (also project-wide sum, which is excluded by the d.name check)
    // since that metric can't be found here, this node is irrelevant
    if (data.ccn === undefined) {
        return relevant;
    }

    // now we're on a relevant node
    relevant.push(data);
    return relevant;
};
