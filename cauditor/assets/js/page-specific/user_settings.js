$( document ).ready(function() {
    // email address multi-input field
    $('#emails').tagsinput({
        tagClass: 'label label-default',
        trimValue: true
    });
    $('#emails')
        .on('beforeItemAdd', function(event) {
            var items = $(this).tagsinput('items').slice(0);
            items.push(event.item);

            $.ajax({
                url: '/api/user/settings',
                method: 'PUT',
                data: JSON.stringify({ 'emails': items.join() })
            }).fail(function() {
                event.cancel;
            });
        })
        .on('beforeItemRemove', function(event) {
            var items = $(this).tagsinput('items').slice(0),
                i = items.indexOf(event.item);
            items.splice(i, 1);

            $.ajax({
                url: '/api/user/settings',
                method: 'PUT',
                data: JSON.stringify({ 'emails': items.join() })
            }).fail(function() {
                event.cancel;
            });
        });
});
