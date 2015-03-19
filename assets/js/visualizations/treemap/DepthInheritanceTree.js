// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.DepthInheritanceTree = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.DepthInheritanceTree.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// anything inheriting from <2 classes is manageable, but then it starts
// to get complex...
Codegraphs.Visualization.Treemap.DepthInheritanceTree.prototype.color = ['dit', [0, 2, 4]];
