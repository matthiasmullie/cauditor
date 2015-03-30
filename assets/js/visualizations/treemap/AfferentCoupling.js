// visualizations/treemap/Class.js must be loaded before this file

Codecharts.Visualization.Treemap.AfferentCoupling = function() {
    Codecharts.Visualization.Treemap.Class.call(this, arguments);
};
Codecharts.Visualization.Treemap.AfferentCoupling.prototype = Object.create(Codecharts.Visualization.Treemap.Class.prototype);

// being used by lots of other packages can signify the class isn't independent enough
// being high means having a lot of impact on the codebase, lots of others depend on you
Codecharts.Visualization.Treemap.AfferentCoupling.prototype.color = ['ca', [0, 5, 10]];
