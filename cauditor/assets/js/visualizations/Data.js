// ../Cauditor.js must be loaded before this file

Cauditor.Data = function(data) {
    this.data = data;
    this.filters = {};
};

/**
 * @param {object} visualization
 * @return {object}
 */
Cauditor.Data.prototype.filter = function(visualization) {
    // results of the callback will be stored in this.filters to avoid having
    // to re-filter the data if we've already done so
    var id = visualization.filter.toString();
    if (!(id in this.filters)) {
        this.filters[id] = visualization.filter(this.data);
    }

    return this.filters[id];
};
