$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $CSRF_TOKEN)
        }
    }
})

$('button#submit').click(function() {
    $.ajax('/register', {
        data: {
            username: $("#username").val(),
            email: $("#email").val(),
        },
        type: 'POST',
        success: function(data) {
            console.log(data);
        },
        error: function(data) {
            console.error(data);
        }
    });
});
