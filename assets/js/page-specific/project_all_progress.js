for (code in jsonUrls) {
    $.ajax({
        url: jsonUrls[code],
        datatype: 'json',
        context: code,
        success: function(data) {
            // all ajax requests are fired at roughly the same time & var `code`
            // (from the loop) will be unreliable in here, because by the time
            // the requests come back, the loop will likely have ended & `code`
            // will contain the last value
            // instead, code is passed as context, so it's available as `this`
            var code = this;

            $(document).ready(function() {
                var selector = '.chart[data-chart-code="'+ code +'"]',
                    range = $(selector).data('chartRange').split(','),
                    chart = new Cauditor(
                        new Cauditor.Visualization.Lineplot.Project(),
                        new Cauditor.Data(data)
                    );

                chart.draw(selector, [code, range, false]);
            });
        }
    });
}


$(document).ready(function() {
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
