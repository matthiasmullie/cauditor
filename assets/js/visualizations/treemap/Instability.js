// visualizations/treemap/Class.js must be loaded before this file

Codegraphs.Visualization.Treemap.Instability = function() {
    Codegraphs.Visualization.Treemap.Class.call(this, arguments);
};
Codegraphs.Visualization.Treemap.Instability.prototype = Object.create(Codegraphs.Visualization.Treemap.Class.prototype);

// range from 0 to 1, with 0 indicating a package very resilient to change in
// dependency classes; 1 being very unstable
// going with green-ish for 75% of the index so only the really problematic
// parts light up (it's pretty easy to score very high on this metric)
Codegraphs.Visualization.Treemap.Instability.prototype.color = [ function(d) {
    // Due to how instability is calculated (ce / (ce + ca)) it's pretty
    // likely to light up red for small classes that have no ca and little
    // ce. Instead of coloring based on the real instability value, I'll
    // change the equation and add 1 to the divisor. For classes without ca,
    // this can drop them significantly if they had little ce; if they have
    // lots of ce and/or ca already, the effect will be minimal.
    // The result of this operation will be that classes with a lot of
    // coupling + instability will light up more than those with lots of
    // instability due to no (or very little) ce.
    return d.ce / (d.ce + d.ca + 1);
}, [0, .75, .85] ];
