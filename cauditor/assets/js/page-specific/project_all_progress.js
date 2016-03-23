$.ajax({
    url: jsonUrl,
    datatype: 'json',
    success: function(data) {
        $( document ).ready(function() {
            $('.chart').each(function() {
                var code = $(this).data('chartCode'),
                    range = $(this).data('chartRange').split(','),
                    chart = new Cauditor(
                        new Cauditor.Visualization.Lineplot.Project(),
                        new Cauditor.Data(data)
                    );

                chart.draw('.chart[data-chart-code='+code+']', [code, range, false]);
            });
        });
    }
});


$( document ).ready(function() {
    $('#expand-panel').click(function() {
        $(this).parent().hide().siblings('.panel-more').show();
        $(this).hide();
    });

    // automatically open the longer description if this is the user's first visit to this page
    if (!document.cookie.match(/(^|;\s*)progress_panel=1($|\s*;)/)) {
        $('#expand-panel').click();
        document.cookie = 'progress_panel=1; expires=Tue, 19 Jan 2038 03:14:08 UTC; path=/';
    }
});
