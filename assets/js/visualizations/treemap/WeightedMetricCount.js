// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.WeightedMetricCount = function() {
    QualityControl.Visualization.Treemap.Class.call(this, arguments);
};
QualityControl.Visualization.Treemap.WeightedMetricCount.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

// make weighted method count start lighting up red if it's > 50, or
// greenish towards 0
// @see http://pdepend.org/documentation/software-metrics/weighted-method-count.html
QualityControl.Visualization.Treemap.WeightedMetricCount.prototype.color = ['wmc', [0, 25, 50]];
