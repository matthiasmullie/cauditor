// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.EfferentCoupling = function() {
    QualityControl.Visualization.Treemap.Class.call(this, arguments);
};
QualityControl.Visualization.Treemap.EfferentCoupling.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

// using lots of other packages can signify the class has too much responsibilities
QualityControl.Visualization.Treemap.EfferentCoupling.prototype.color = ['ce', [0, 10, 20]];
