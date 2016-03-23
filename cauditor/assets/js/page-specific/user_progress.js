$.ajax({
    url: '/api/user/diffs',
    datatype: 'json',
    success: function(data) {
        $(document).ready(function() {
            var $element = $('.chart'),
                code = $element.data('chartCode'),
                basis = $element.data('chartBasis'),
                range = $element.data('chartRange').split(','),
                chart = new Cauditor(
                    new Cauditor.Visualization.Lineplot.User(),
                    new Cauditor.Data(data)
                );

            chart.draw('.chart', [code, range]);
        });
    }
});
