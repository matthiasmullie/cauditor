// visualizations/treemap/Method.js must be loaded before this file

QualityControl.Visualization.Treemap.NpathComplexity = function() {
    QualityControl.Visualization.Treemap.Method.call(this, arguments);
};
QualityControl.Visualization.Treemap.NpathComplexity.prototype = Object.create(QualityControl.Visualization.Treemap.Method.prototype);

// 0-100: green to yellow; 100-200: orange to red; 200+: red
// @see http://pdepend.org/documentation/software-metrics/cyclomatic-complexity.html
QualityControl.Visualization.Treemap.NpathComplexity.prototype.color = ['npath', [0, 100, 200]];
