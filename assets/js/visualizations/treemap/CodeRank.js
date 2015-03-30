// visualizations/treemap/Class.js must be loaded before this file

Codecharts.Visualization.Treemap.CodeRank = function() {
    Codecharts.Visualization.Treemap.Class.call(this, arguments);
};
Codecharts.Visualization.Treemap.CodeRank.prototype = Object.create(Codecharts.Visualization.Treemap.Class.prototype);

// code rank of <0.5 is pretty safe, not referenced too much
Codecharts.Visualization.Treemap.CodeRank.prototype.color = ['cr', [0.15, .5, 1]];
