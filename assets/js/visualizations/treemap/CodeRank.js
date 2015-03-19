// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.CodeRank = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.CodeRank.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// code rank of <0.5 is pretty safe, not referenced too much
Codegraphs.Visualization.Treemap.CodeRank.prototype.color = ['cr', [0.15, .5, 1]];
