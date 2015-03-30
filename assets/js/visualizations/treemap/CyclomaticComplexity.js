// visualizations/treemap/Method.js must be loaded before this file

Codecharts.Visualization.Treemap.CyclomaticComplexity = function() {
    Codecharts.Visualization.Treemap.Method.call(this, arguments);
};
Codecharts.Visualization.Treemap.CyclomaticComplexity.prototype = Object.create(Codecharts.Visualization.Treemap.Method.prototype);

// 1-4 green-ish; 5-7 yellow-ish; 8-10: orange-ish; 10+: red
// @see http://phpmd.org/rules/codesize.html#npathcomplexity
Codecharts.Visualization.Treemap.CyclomaticComplexity.prototype.color = ['ccn', [0, 6, 11]];
