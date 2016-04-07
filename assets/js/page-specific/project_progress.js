$.ajax({
    url: jsonUrl,
    datatype: 'json',
    success: function(data) {
        $(document).ready(function() {
            var $element = $('.chart'),
                code = $element.data('chartCode'),
                range = $element.data('chartRange').split(','),
                chart = new Cauditor(
                    new Cauditor.Visualization.Lineplot.Project(),
                    new Cauditor.Data(data)
                );

            chart.draw('.chart', [code, range]);
        });
    }
});
