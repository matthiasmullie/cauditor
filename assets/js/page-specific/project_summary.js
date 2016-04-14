var promise;

$.ajax({
    url: jsonUrlMetrics,
    datatype: 'json',
    success: function(data) {
        $(document).ready(function() {
            var $element = $('.chart'),
                code = $element.data('chartCode'),
                basis = $element.data('chartBasis'),
                range = $element.data('chartRange').split(','),
                chart = new Cauditor(
                    new Cauditor.Visualization.Treemap.Method(),
                    new Cauditor.Data(data)
                );

            chart.draw('.chart[data-chart-code='+code+']', [code, range, false]);
        });
    }
});

$(document).ready(function() {
    $('.load-more a').click(function(e) {
        var element = this;

        e.preventDefault();

        if (!promise) {
            promise = $.ajax({
                url: jsonUrlCommits,
                datatype: 'json'
            });
        }

        // we've started fetching this data on pageload already (for some chart), but
        // it may not yet be available, so indicate that we're actually doing something!
        $(this).after(' <i class="fa fa-spinner fa-spin"></i>');

        promise
            .always(function() {
                // success or failure, get rid of that spinner!
                $(element).next('.fa-spinner').remove();
            })
            .done(function(commits) {
                var count = 0, map = {};

                // sort on date: newest first
                commits.sort(function(a, b) {
                    return a.timestamp < b.timestamp ? 1 : -1;
                });

                // the next commit (datewise) may not actually be the next one;
                // our timestamp is author timestamp
                // we'll want to find the real previous commit (for which we have
                // the hash), so having a map to locate it will be useful
                for (i in commits) {
                    map[commits[i].hash] = commits[i];
                }

                for (i in commits) {
                    if (hashes.indexOf(commits[i].hash) < 0) {
                        hashes.push(commits[i].hash);

                        append.call(
                            $(element).closest('tr').get(0),
                            commits[i],
                            map[commits[i].previous] || {}
                        );

                        if (++count >= batch) {
                            return;
                        }
                    }
                }

                // if we make it here, there are no commits left - let's check if this is actually the first commit!
                if (commits[commits.length - 1].previous) {
                    $(element).closest('tr').before(
                        '<tr>' +
                            '<td colspan="8" class="col-xs-12 text-center">' +
                                'Commit history is incomplete. Missing commits should be imported soon! ' +
                                'Or <a href="/help/import">bypass the import queue and submit them yourself</a>.' +
                            '</td>' +
                        '</tr>'
                    );
                }

                // no more commits left; get rid of "load more" link
                $(element).closest('tr').remove();
            });
    });
});

function append(commit, prev) {
    var indicator = '', classname = '', score, prev_score;
    if (prev) {
        score = commit.weighed_mi;
        prev_score = prev.weighed_mi;
        if (score > prev_score) {
            indicator = '<i class="fa fa-caret-up green-text"></i>';
            classname = 'positive';
        } else if (score < prev_score) {
            indicator = '<i class="fa fa-caret-down red-text"></i>';
            classname = 'negative';
        }
    }

    $(this).before(
        '<tr class="' + classname + '">' +
            '<td class="col-xs-1 text-center">' + indicator + '</td>' +
            '<td class="col-xs-2">' +
                '<i class="fa fa-code"></i>' +
                '<strong>' +
                    '<a href="/' + commit.project + '/' + commit.hash + '/metrics">' + commit.hash.substr(0, 7) + '</a><br />' +
                '</strong>' +
            '</td>' +
            '<td class="col-xs-2">' +
                '<i class="fa fa-code-fork"></i>' +
                    commit.branch +
            '</td>' +
            '<td class="col-xs-3">' + commit.timestamp.replace('T', ' ') + '</td>' +
            '<td class="col-xs-1">' + commit.weighed_mi + '</td>' +
            '<td class="col-xs-1">' + commit.worst_mi + '</td>' +
            '<td class="col-xs-2 text-center">' +
                '<a href="/' + commit.project + '/' + commit.hash + '/metrics">Metrics <i class="fa fa-long-arrow-right"></i></a>' +
            '</td>' +
        '</tr>'
    );
}
