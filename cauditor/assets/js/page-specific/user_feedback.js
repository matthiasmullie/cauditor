var questions = {
    'How fast does %s work?': ['Slow', 'Fast'],
    'Does %s have an eye for detail?': ['Not so much', 'Very thorough'],
    'Does %s cause a lot of bugs?': ['Few bugs', 'Lots of bugs'],
    'How much experience does %s have?': ['Junior', 'Senior'],
    "How would you rate %s's knowledge?": ['Theoretical', 'Practical'],
    'Does %s usually fix issues in existing code, or build new features': ['Fix existing code', 'Build new features'],
    'Does %s usually take the lead on new developments?': ['No', 'Yes'],
    'Is %s a team player?': ['No', 'Yes'],
    'Does %s architect new features, or does (s)he implement as directed by someone else?': ['Architect', 'Implementer'],
    "How would you characterize %s's code?": ['Oversimplified', 'Overengineered'],
    'Has %s received formal education in software engineering?': ['Self-taught', 'Computer Science degree'],
    'Does %s write tests for the majority of their code?': ['No tests', 'TDD']
}, colleagues = [], data = {};

$.ajax({
    url: '/api/user/colleagues',
    datatype: 'json',
    success: function(data) {
        $(document).ready(function() {
            if (data.length === 0) {
                $('form').replaceWith(
                    '<div class="row">' +
                        '<div class="col-xs-12 columns">' +
                            '<div class="alert alert-danger" role="alert">' +
                                '<i class="fa fa-exclamation-circle"></i>' +
                                "Thank you for wanting to help out, but we couldn't find anyone for you to rate at this point. Please check back later!" +
                            '</div>' +
                        '</div>' +
                    '</div>'
                );
                return;
            }

            colleagues = data;

            $('form input.rating').on('change', function () {
                submit();
                render();
            });
            $('form button.skip').on('click', function () {
                render();
            });

            render();
        });
    }
});

function render() {
    var colleague = colleagues[Math.floor(Math.random() * colleagues.length)],
        qs = Object.keys(questions),
        question = qs[Math.floor(Math.random() * qs.length)],
        $form = $('form'),
        buttons = questions[question];

    // visual
    $form.find('h3').text(colleague.project);
    $form.find('p').html(question.replace('%s', '<strong>' + colleague.author + '</strong>'));
    $form.find('.left').html(buttons[0]);
    $form.find('.right').html(buttons[1]);
    // reset stars
    $form.find('.rating').rating('rate', 0);

    // data to submit
    $form.find('input[name=question]').val(question);
    $form.find('input[name=project]').val(colleague.project);
    $form.find('input[name=author]').val(colleague.author);
}

function submit(project, colleague, question, answer) {
    var data = $('form').serializeArray(), values = {}, i;

    for (i in data) {
        values[data[i].name] = data[i].value;
    }

    $.ajax({
        url: '/api/user/feedback',
        method: 'PUT',
        data: JSON.stringify(values)
    });
}
