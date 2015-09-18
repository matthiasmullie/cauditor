// ../Caudit.js must be loaded before this file

Caudit.Data = function(data) {
    this.data = data;
    this.filters = {};
};

/**
 * @param {function} callback
 * @return {object}
 */
Caudit.Data.prototype.filter = function(callback) {
    // results of the callback will be stored in this.filters to avoid having
    // to re-filter the data if we've already done so
    var id = callback.toString();
    if (!(id in this.filters)) {
        this.filters[id] = callback(this.data);
    }

    return this.filters[id];
};
