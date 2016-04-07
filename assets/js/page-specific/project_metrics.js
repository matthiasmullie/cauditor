$.ajax({
    url: jsonUrl,
    datatype: 'json',
    jsonp: false,
    cache: true,
    success: function(data) {
        $(document).ready(function() {
            var $element = $('.chart'),
                code = $element.data('chartCode'),
                basis = $element.data('chartBasis'),
                range = $element.data('chartRange').split(','),
                chart = new Cauditor(
                    basis === 'method' ? new Cauditor.Visualization.Treemap.Method() : new Cauditor.Visualization.Treemap.Class(),
                    new Cauditor.Data(data)
                );

            chart.draw('.chart', [code, range]);
        });
    }
});
