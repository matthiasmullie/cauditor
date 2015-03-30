// visualizations/treemap/Class.js must be loaded before this file

Codecharts.Visualization.Treemap.DepthInheritanceTree = function() {
    Codecharts.Visualization.Treemap.Class.call(this, arguments);
};
Codecharts.Visualization.Treemap.DepthInheritanceTree.prototype = Object.create(Codecharts.Visualization.Treemap.Class.prototype);

// anything inheriting from <2 classes is manageable, but then it starts
// to get complex...
Codecharts.Visualization.Treemap.DepthInheritanceTree.prototype.color = ['dit', [0, 2, 4]];
