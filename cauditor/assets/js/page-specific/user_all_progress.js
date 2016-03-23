$.ajax({
    url: '/api/user/diffs',
    datatype: 'json',
    success: function(data) {
        $( document ).ready(function() {
            if (!data) {
                $('.no-commits').show();
            } else {
                var chart = new Cauditor(
                    new Cauditor.Visualization.Lineplot.User(),
                    new Cauditor.Data(data)
                ), charts = [], metrics = {}, include, median;

                $('.chart').each(function() {
                    var code = $(this).data('chartCode'),
                        basis = $(this).data('chartBasis'),
                        range = $(this).data('chartRange').split(',');

                    chart.draw('.chart[data-chart-code='+code+']', [code, range, false]);

                    charts.push(code);
                });

                // loop all commits, figure out which we want to include & add their relevant values to `metrics`
                for (i in data) {
                    include = false;
                    // we only want to include commits where at least 1 metric was affected; otherwise they likely weren't code changes
                    for (i in charts) {
                        include = include || data[i][charts[i]] !== 0;
                    }

                    if (include) {
                        for (i in charts) {
                            metrics[charts[i]] = metrics[charts[i]] || [];
                            metrics[charts[i]].push(data[i][charts[i]]);
                        }
                    }
                }

                // now that we have values for all metrics, fetch the median value & add to title
                for (metric in metrics) {
                    // sort on metric scores, so we can easily grab median
                    metrics[metric].sort(function(a, b) {
                        return a > b ? 1 : -1;
                    });

                    median = metrics[metric][Math.floor(metrics[metric].length / 2)];
                    median = Math.round(median * 10000) / 10000;
                    $('#' + metric + ' h2').append(': <span style="text-transform: none">' + median + ' median</span>');
                }
            }
        });
    }
});
