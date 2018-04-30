function ProjectAjaxSuccess(project_form, post_form){
    if (!project_form.hasClass('hideelement')){
        project_form.addClass('hideelement');
    }

    if (post_form.hasClass('hideelement')){
        post_form.removeClass('hideelement');
    }
}

/*
function ProjectAjaxError(jqXHR, textStatus, errorThrown){
    console.log(jqXHR)
    console.log(textStatus)
    console.log(errorThrown)
}
*/

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

$("#SaveCreate").click(function(event){

    event.preventDefault();

    var project_form = $(document.getElementById('ProjectForm'));
    var post_form = $(document.getElementById('PostForm'));

    var button = $(event.target); // Button that triggered the modal
    var $thisURL = project_form.attr('data-url') || window.location.href // or set your own url
    var $formData = project_form.serialize();

    $.ajax({
        method: "POST",
        url: $thisURL,
        data: $formData,
        beforeSend: clear_form_field_errors(project_form),
        success: function(data){
            console.log(data);
            ProjectAjaxSuccess(project_form, post_form);
            },
        error: ProjectAjaxError,
    })
});

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

/*
$(document).ready(function(){

    var project_form = $(document.getElementById('ProjectForm'));
    var post_form = $(document.getElementById('PostForm'));

    post_form.submit(function(event){
        event.preventDefault()

        var ProjectformData = project_form.serialize();

        console.log(ProjectformData);

        var Projectform_url = ProjectformData.attr('data-url') || window.location.href // or set your own url

        console.log(Projectform_url);

        $.ajax({
            method: "POST",
            url: Projectform_url,
            data: ProjectformData,
            success: handleFormSuccess,
            error: handleFormError,
        })


        var postformData = $(this).serialize()
        var postform_url = postformData.attr('data-url') || window.location.href // or set your own url

        console.log(postform_url);

        $.ajax({
            method: "POST",
            url: postform_url,
            data: postformData,
            success: handleFormSuccess,
            error: handleFormError,
        })

        // document.getElementById("PostForm").reset(); // reset form data
        // document.getElementById("ProjectForm").reset(); // reset form data

    })

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)

    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
    }
})
*/

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});