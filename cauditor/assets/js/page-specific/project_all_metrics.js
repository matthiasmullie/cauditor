$.ajax({
    url: jsonUrl,
    datatype: 'json',
    jsonp: false,
    cache: true,
    success: function(data) {
        $( document ).ready(function() {
            $('.chart').each(function() {
                var code = $(this).data('chartCode'),
                    basis = $(this).data('chartBasis'),
                    range = $(this).data('chartRange').split(','),
                    chart = new Cauditor(
                        basis === 'method' ? new Cauditor.Visualization.Treemap.Method() : new Cauditor.Visualization.Treemap.Class(),
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
    if (!document.cookie.match(/(^|;\s*)metrics_panel=1($|\s*;)/)) {
        $('#expand-panel').click();
        document.cookie = 'metrics_panel=1; expires=Tue, 19 Jan 2038 03:14:08 UTC; path=/';
    }
});
