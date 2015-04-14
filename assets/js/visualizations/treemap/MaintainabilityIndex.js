// visualizations/treemap/Method.js must be loaded before this file

QualityControl.Visualization.Treemap.MaintainabilityIndex = function() {
    QualityControl.Visualization.Treemap.Method.call(this, arguments);
};
QualityControl.Visualization.Treemap.MaintainabilityIndex.prototype = Object.create(QualityControl.Visualization.Treemap.Method.prototype);

// 100-20 is considered ok; 20-10 suspicious; 10-0 bad
// given the long green range and very low threshold, things can start to turn orange-ish a bit earlier
// @see http://blogs.msdn.com/b/codeanalysis/archive/2007/11/20/maintainability-index-range-and-meaning.aspx
QualityControl.Visualization.Treemap.MaintainabilityIndex.prototype.color = ['mi', [75, 30, 20]];
