// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.AfferentCoupling = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.AfferentCoupling.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// being used by lots of other packages can signify the class isn't independent enough
// being high means having a lot of impact on the codebase, lots of others depend on you
Codegraphs.Visualization.Treemap.AfferentCoupling.prototype.color = ['ca', [0, 5, 10]];
