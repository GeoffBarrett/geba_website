// Takes field name and error, finds the field on page and sets error text to the passed in error
function apply_form_field_error(fieldname, error) {
    var input = $("#id_" + fieldname),
        container = $("#div_id_" + fieldname),
        label = $('label[for="id_' + fieldname + '"]'),
        //error_span = $("span#error_id_" + fieldname);
        //error_span.addClass("help-inline ajax-error").text(error[0]);
        error_div = $("div#error_id_" + fieldname);
        error_msg = $("<span />").addClass("text-danger small help-inline ajax-error").text(error[0]);

    error_div.html(error_msg);
    label.addClass("test");
    container.addClass("error");
    // error_msg.insertAfter(input);

}

// removes the error message given, should run this before every AJAX submission
function clear_form_field_errors(form) {
    $(".ajax-error", $(form)).remove();
    $(".error", $(form)).removeClass("error");
}


function django_message(msg, level) {
    var levels = {
        warning: 'alert',
        error: 'error',
        success: 'success',
        info: 'info'
    },
    source = $('#message_template').html(),
    template = Handlebars.compile(source),
    context = {
        'tags': levels[level],
        'message': msg
    },
    html = template(context);

    $("#message_area").append(html);
}

function django_block_message(msg, level) {
    var source = $("#message_block_template").html(),
        template = Handlebars.compile(source),
        context = {level: level, body: msg},
        html = template(context);

    $("#message_area").append(html);
}