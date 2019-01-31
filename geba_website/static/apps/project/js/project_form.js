function ProjectAjaxSuccess(project_form, post_form){
    if (!project_form.hasClass('hideelement')){
        project_form.addClass('hideelement');
    }

    if (post_form.hasClass('hideelement')){
        post_form.removeClass('hideelement');
    }
}

function ProjectAjaxError(data, textStatus, jqXHR){
    var errors = $.parseJSON(data.responseText);
    $.each(errors, function(index, value) {
        if (index === "__all__") {
            django_message(value[0], "error");
        } else {
            apply_form_field_error(index, value);
        }
    });
}


$("#BackProject").click(function(event){
    event.preventDefault();

    var project_form = $(document.getElementById('ProjectForm'));
    var post_form = $(document.getElementById('PostForm'));

    var button = $(event.target); // Button that triggered the modal

    var save_url = button.data('href');

    if (!post_form.hasClass('hideelement')){
        post_form.addClass('hideelement');
    }

    if (project_form.hasClass('hideelement')){
        project_form.removeClass('hideelement');
    }

});