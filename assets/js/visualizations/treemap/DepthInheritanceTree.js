// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.DepthInheritanceTree = function() {
    QualityControl.Visualization.Treemap.Class.call(this, arguments);
};
QualityControl.Visualization.Treemap.DepthInheritanceTree.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

// anything inheriting from <2 classes is manageable, but then it starts
// to get complex...
QualityControl.Visualization.Treemap.DepthInheritanceTree.prototype.color = ['dit', [0, 2, 4]];
