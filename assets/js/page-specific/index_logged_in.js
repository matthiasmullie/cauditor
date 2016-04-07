for (project in jsonUrls) {
    $.ajax({
        url: jsonUrls[project],
        datatype: 'json',
        context: project,
        success: function(data) {
            // all ajax requests are fired at roughly the same time & var `project`
            // (from the loop) will be unreliable in here, because by the time
            // the requests come back, the loop will likely have ended & `project`
            // will contain the last value
            // instead, project is passed as context, so it's available as `this`
            var project = this;

            $(document).ready(function() {
                var $element = $('#'+ project.replace('/', '_') +' .chart'),
                    code = $element.data('chartCode'),
                    basis = $element.data('chartBasis'),
                    range = $element.data('chartRange').split(','),
                    chart = new Cauditor(
                        new Cauditor.Visualization.Treemap.Method(),
                        new Cauditor.Data(data)
                    );

                chart.draw('#'+ project.replace('/', '_') +' .chart[data-chart-code='+code+']', [code, range, false]);
            });
        }
    });
}
