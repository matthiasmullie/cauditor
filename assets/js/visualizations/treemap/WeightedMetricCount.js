// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.WeightedMetricCount = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.WeightedMetricCount.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// make weighted method count start lighting up red if it's > 50, or
// greenish towards 0
// @see http://pdepend.org/documentation/software-metrics/weighted-method-count.html
Codegraphs.Visualization.Treemap.WeightedMetricCount.prototype.color = ['wmc', [0, 25, 50]];
