// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.CodeRank = function() {
    QualityControl.Visualization.Treemap.Class.call(this, arguments);
};
QualityControl.Visualization.Treemap.CodeRank.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

// code rank of <0.5 is pretty safe, not referenced too much
QualityControl.Visualization.Treemap.CodeRank.prototype.color = ['cr', [0.15, .5, 1]];
