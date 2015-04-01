// visualizations/treemap/Class.js must be loaded before this file

QualityControl.Visualization.Treemap.AfferentCoupling = function() {
    QualityControl.Visualization.Treemap.Class.call(this, arguments);
};
QualityControl.Visualization.Treemap.AfferentCoupling.prototype = Object.create(QualityControl.Visualization.Treemap.Class.prototype);

// being used by lots of other packages can signify the class isn't independent enough
// being high means having a lot of impact on the codebase, lots of others depend on you
QualityControl.Visualization.Treemap.AfferentCoupling.prototype.color = ['ca', [0, 5, 10]];
