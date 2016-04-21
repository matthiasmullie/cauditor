$(document).ready(function() {
    // link/unlink projects
    $('.switch input')
        .bootstrapSwitch({ size: 'mini' })
        .on('switchChange.bootstrapSwitch', function(e, state) {
            var language = $(this).data('language'),
                $switch = $(this),
                $row = $switch.closest('.repo');

            $row.next('.link-success, .link-failure').remove();

            // ask confirmation when trying to link a non-PHP project
            if (
                state &&
                language !== 'PHP' &&
                !confirm("Uh-oh! GitHub doesn't seem to think this is a PHP project. Unfortunately, that's all we can currently generate metrics for. Are you sure you want to continue analyzing PHP code in this repo?")
            ) {
                $switch.bootstrapSwitch('state', false, true);
                return false;
            }

            $.ajax({
                url: '/api/user/link/' + $(this).data('repo'),
                method: 'PUT',
                data: JSON.stringify({
                    repo: $(this).data('repo'),
                    action: state ? 'link' : 'unlink'
                })
            })
            .done(function(data) {
                // there may be multiple switches for the same repo (e.g. in the list & the one in the intro)
                // so let's make sure that when one is switched, the other's state is also updated
                $('input[data-repo="'+ $(e.target).data('repo') +'"]')
                    .each(function() {
                        var $checkbox = $(this),
                            $row = $checkbox.closest('.repo'),
                            $title = $row.find('.title'),
                            text = '<strong>Success!</strong> Check <a href="'+ data.name +'">your analysis</a>. Or do you want to <a href="/help/import#ci">customize your config</a>? Or skip the busy Cauditor import queue and <a href="/help/import#bin">let your CI build push the metrics</a>?';

                        if (state) {
                            // we just linked the repo
                            $title.wrap('<a href="/'+ data.name +'"></a>');

                            $title.closest('td').append(' <a class="btn btn-primary btn-xs" href="/'+ data.name +'" role="button"><i class="fa fa-line-chart"></i></a>');

                            if ($row.is('tr')) {
                                $row.after('<tr class="link-success">'+
                                    '<td class="col-xs-12 alert alert-warning text-center" colspan="5">'+ text +'</td>'+
                                '</tr>');
                            } else {
                                $row.after('<p>'+ text + '</p>');
                            }
                        } else {
                            // we just unlinked the repo
                            $title.unwrap('<a href="/'+ data.name +'"></a>');
                            $title.parent().find('.btn').remove();
                        }
                    })
                    // ensure state is updated for all switches
                    .bootstrapSwitch('state', state, true);
            })
            .fail(function() {
                var $checkbox = $(e.target),
                    $row = $checkbox.closest('.repo');

                    // toggle back on failure
                    $switch.bootstrapSwitch('toggleState', true);

                    $row.after('<tr class="link-failure">' +
                        '<td class="col-xs-12 alert alert-danger text-center" colspan="5">' +
                            '<strong>Failed!</strong> Please try again, or <a href="https://github.com/cauditor/issues/issues/new">submit a bug report</a> if the problem persists.' +
                        '</td>' +
                    '</tr>');
            });
        });


    // refresh list of repos
    $.ajax({
        url: '/api/user/repos',
        method: 'GET'
    })
    .done(function(data) {
        var existing = [],
            current = data.map(function(repo) {
                return repo.name;
            });

        $('.repo input[data-repo]').each(function() {
            existing.push($(this).data('repo'));
        });
        existing = $.unique(existing);

        if (existing.sort().toString() !== current.sort().toString()) {
            // @todo: ideally, I would re-render in-page, not refresh
            location.reload();
        }
    });
});
