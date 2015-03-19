// visualizations/treemap/Method.js must be loaded before this file

Codegraphs.Visualization.Treemap.CyclomaticComplexity = function() {
    Codegraphs.Visualization.Treemap.Method.call(this, arguments);
};
Codegraphs.Visualization.Treemap.CyclomaticComplexity.prototype = Object.create(Codegraphs.Visualization.Treemap.Method.prototype);

// 1-4 green-ish; 5-7 yellow-ish; 8-10: orange-ish; 10+: red
// @see http://phpmd.org/rules/codesize.html#npathcomplexity
Codegraphs.Visualization.Treemap.CyclomaticComplexity.prototype.color = ['ccn', [0, 6, 11]];
