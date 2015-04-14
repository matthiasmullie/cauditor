// visualizations/treemap/Abstract.js must be loaded before this file

QualityControl.Visualization.Treemap.Class = function() {
    QualityControl.Visualization.Treemap.Abstract.call(this, arguments);
};
QualityControl.Visualization.Treemap.Class.prototype = Object.create(QualityControl.Visualization.Treemap.Abstract.prototype);

/**
 * Callback method transforming data to however 'visualization' needs it.
 *
 * @param {object} data
 * @return {object}
 */
QualityControl.Visualization.Treemap.Class.prototype.data = function(data) {
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

        return true;
    });
};

QualityControl.Visualization.Treemap.Class.prototype.id = ['package', 'name'];
QualityControl.Visualization.Treemap.Class.prototype.tooltip = ['loc', 'ca', 'ce', 'i', 'dit'];
