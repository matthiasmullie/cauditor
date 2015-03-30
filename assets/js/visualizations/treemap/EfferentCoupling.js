// visualizations/treemap/Class.js must be loaded before this file

Codecharts.Visualization.Treemap.EfferentCoupling = function() {
    Codecharts.Visualization.Treemap.Class.call(this, arguments);
};
Codecharts.Visualization.Treemap.EfferentCoupling.prototype = Object.create(Codecharts.Visualization.Treemap.Class.prototype);

// using lots of other packages can signify the class has too much responsibilities
Codecharts.Visualization.Treemap.EfferentCoupling.prototype.color = ['ce', [0, 10, 20]];
