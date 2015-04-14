// visualizations/treemap/Method.js must be loaded before this file

QualityControl.Visualization.Treemap.HalsteadEffort = function() {
    QualityControl.Visualization.Treemap.Method.call(this, arguments);
};
QualityControl.Visualization.Treemap.HalsteadEffort.prototype = Object.create(QualityControl.Visualization.Treemap.Method.prototype);

QualityControl.Visualization.Treemap.HalsteadEffort.prototype.color = ['he', [0, 5000, 10000]];
