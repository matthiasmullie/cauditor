for (project in jsonUrls) {
    $.ajax({
        url: jsonUrls[project],
        datatype: 'json',
        success: function(data) {
            $( document ).ready(function() {
                var $element = $('#'+ project.replace('/', '_') +' .chart'),
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
}
