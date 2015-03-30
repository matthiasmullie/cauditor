// visualizations/treemap/Method.js must be loaded before this file

Codecharts.Visualization.Treemap.NpathComplexity = function() {
    Codecharts.Visualization.Treemap.Method.call(this, arguments);
};
Codecharts.Visualization.Treemap.NpathComplexity.prototype = Object.create(Codecharts.Visualization.Treemap.Method.prototype);

// 0-100: green to yellow; 100-200: orange to red; 200+: red
// @see http://pdepend.org/documentation/software-metrics/cyclomatic-complexity.html
Codecharts.Visualization.Treemap.NpathComplexity.prototype.color = ['npath', [0, 100, 200]];
