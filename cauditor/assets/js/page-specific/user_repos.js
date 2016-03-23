$( document ).ready(function() {
    // link/unlink projects
    $('.switch input')
        .bootstrapSwitch({ size: 'mini' })
        .on('switchChange.bootstrapSwitch', function(e, state) {
            var language = $(this).closest('.repo').find('.code-language').text();

            // ask confirmation when trying to link a non-PHP project
            if (
                state &&
                language !== 'PHP' &&
                !confirm("Uh-oh! GitHub doesn't seem to think this is a PHP project. Unfortunately, that's all we can currently generate metrics for. Are you sure you want to continue analyzing PHP code in this repo?")
            ) {
                $(this).bootstrapSwitch('state', false, true);
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
                var $checkbox = $(e.target),
                    $row = $checkbox.closest('.repo'),
                    $title = $row.find('.title'),
                    msg;

                if (state) {
                    // we just linked the repo
                    $title.wrap('<a href="/'+ data.name +'"></a>');
                    $checkbox.closest('.switch').append('<a class="btn btn-primary btn-xs" href="/'+ data.name +'" role="button"><i class="fa fa-line-chart"></i></a>');

                    $row.after('<tr class="link-success">' +
                        '<td class="col-xs-12 alert alert-warning text-center" colspan="5">' +
                            '<strong>Success!</strong> Do you want to <a href="/help/import#ci">customize your configuration</a>? Or skip the busy Cauditor import queue and <a href="/help/import#bin">let your CI build push the metrics</a>?' +
                        '</td>' +
                    '</tr>');
                } else {
                    // we just unlinked the repo
                    $title.unwrap('<a href="/'+ data.name +'"></a>');
                    $checkbox.closest('.switch').find('.btn').remove();

                    $row.next('.link-success').remove();
                }
            })
            .fail(function() {
                // @todo better error handling; this is piss-poor!
                alert('Failed to link project & this error handling is extremely poor! Try logging in again?');
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

        $('.repo').each(function() {
            existing.push($(this).data('repo'));
        });

        if (existing.sort().toString() !== current.sort().toString()) {
            // @todo: ideally, I would re-render in-page, not refresh
            location.reload();
        }
    });
});
