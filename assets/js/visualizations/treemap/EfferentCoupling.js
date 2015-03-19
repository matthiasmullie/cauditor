// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.EfferentCoupling = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.EfferentCoupling.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// using lots of other packages can signify the class has too much responsibilities
Codegraphs.Visualization.Treemap.EfferentCoupling.prototype.color = ['ce', [0, 10, 20]];
