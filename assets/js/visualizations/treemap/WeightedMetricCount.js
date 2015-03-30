// visualizations/treemap/Class.js must be loaded before this file

Codecharts.Visualization.Treemap.WeightedMetricCount = function() {
    Codecharts.Visualization.Treemap.Class.call(this, arguments);
};
Codecharts.Visualization.Treemap.WeightedMetricCount.prototype = Object.create(Codecharts.Visualization.Treemap.Class.prototype);

// make weighted method count start lighting up red if it's > 50, or
// greenish towards 0
// @see http://pdepend.org/documentation/software-metrics/weighted-method-count.html
Codecharts.Visualization.Treemap.WeightedMetricCount.prototype.color = ['wmc', [0, 25, 50]];
