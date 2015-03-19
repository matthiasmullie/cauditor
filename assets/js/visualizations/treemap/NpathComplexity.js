// visualizations/treemap/Method.js must be loaded before this file

Codegraphs.Visualization.Treemap.NpathComplexity = function() {
    Codegraphs.Visualization.Treemap.Method.call(this, arguments);
};
Codegraphs.Visualization.Treemap.NpathComplexity.prototype = Object.create(Codegraphs.Visualization.Treemap.Method.prototype);

// 0-100: green to yellow; 100-200: orange to red; 200+: red
// @see http://pdepend.org/documentation/software-metrics/cyclomatic-complexity.html
Codegraphs.Visualization.Treemap.NpathComplexity.prototype.color = ['npath', [0, 100, 200]];
