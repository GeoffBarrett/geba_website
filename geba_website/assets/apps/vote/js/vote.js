// this script is for upvoting
$('.upvote-btn').click(function(event){

    event.preventDefault();

    var button = $(event.target); // Button that triggered the modal
    var vote = $(this);
    var current_class_obj = vote.parent().parent();
    var current_class = current_class_obj.attr('current_class');
    var object = button.data('object');
    var like_url = button.data('href');

    if (like_url == '#'){
        return;
    }

    vote.parent().removeClass(current_class);  // removes whatever the current class is

    if(current_class == "unvoted"){
        // the class is not likes

        vote.parent().addClass("likes");  // adds the likes class
        current_class_obj.attr('current_class', 'likes');

        button.removeClass('up');
        button.addClass('upmod');

    } else if (current_class == 'dislikes'){

        other_vote_button = vote.parent().find('.arrow.downmod');
        other_vote_button.removeClass('downmod');
        other_vote_button.addClass('down');

        vote.parent().addClass('likes');  // adds the likes class
        current_class_obj.attr('current_class', 'likes');
        button.removeClass('up');
        button.addClass('upmod');

    } else {
        // the class is likes, so unlike

        vote.parent().addClass('unvoted');  // adds the unvoted class
        current_class_obj.attr('current_class', 'unvoted');

        if(button.hasClass('upmod')){
            button.removeClass('upmod');
            button.addClass('up');
        }
    }

    $.ajax({
        url: like_url,
        method: "GET",
        data: {},
        success: handleFormSuccess,
        error: handleFormError
    })

})

// this script is for upvoting
$('.upvote-btn-mobile').click(function(event){

    event.preventDefault();

    var button = $(event.target); // Button that triggered the modal
    var vote = $(this);
    var current_class_obj = vote.parent().parent();
    var current_class = current_class_obj.attr('current_class');
    var object = button.data('object');
    var like_url = button.data('href');

    if (like_url == '#'){
        return;
    }

    vote.parent().removeClass(current_class + '-mobile');  // removes whatever the current class is

    if(current_class == "unvoted"){
        // the class is not likes

        vote.parent().addClass("likes-mobile");  // adds the likes class
        current_class_obj.attr('current_class', 'likes');

        button.removeClass('up');
        button.addClass('upmod');

    } else if (current_class == 'dislikes'){

        other_vote_button = vote.parent().find('.arrow.downmod');
        other_vote_button.removeClass('downmod');
        other_vote_button.addClass('down');

        vote.parent().addClass('likes-mobile');  // adds the likes class
        current_class_obj.attr('current_class', 'likes');
        button.removeClass('up');
        button.addClass('upmod');

    } else {
        // the class is likes, so unlike

        vote.parent().addClass('unvoted-mobile');  // adds the unvoted class
        current_class_obj.attr('current_class', 'unvoted');

        if(button.hasClass('upmod')){
            button.removeClass('upmod');
            button.addClass('up');
        }
    }

    $.ajax({
        url: like_url,
        method: "GET",
        data: {},
        success: handleFormSuccess,
        error: handleFormError
    })

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



// this script is for downvoting
$('.downvote-btn').click(function(event){

    event.preventDefault();
    var button = $(event.target); // Button that triggered the modal
    var vote = $(this);
    var current_class_obj = vote.parent().parent();
    var current_class = current_class_obj.attr('current_class');
    var object = button.data('object');
    var dislike_url = button.data('href');

    if (dislike_url == '#'){
        return;
    }

    vote.parent().removeClass(current_class);  // removes whatever the current class is

    if(current_class == "unvoted"){
        // the class is not dislikes

        vote.parent().addClass('dislikes');  // adds the likes class
        current_class_obj.attr('current_class', 'dislikes');
        button.removeClass('down');
        button.addClass('downmod');


    } else if (current_class == 'likes'){

        other_vote_button = vote.parent().find('.arrow.upmod');
        other_vote_button.removeClass('upmod');
        other_vote_button.addClass('up');

        vote.parent().addClass('dislikes');  // adds the likes class
        current_class_obj.attr('current_class', 'dislikes');
        button.removeClass('down');
        button.addClass('downmod');

    } else {
        // the class is dislikes, so un-dislike

        vote.parent().addClass("unvoted");  // adds the unvoted class
        current_class_obj.attr('current_class', 'unvoted');

        if(button.hasClass('downmod')){
            button.removeClass('downmod');
            button.addClass('down');
        }
    }

    $.ajax({
        url: dislike_url,
        method: "GET",
        data: {},
        success: handleFormSuccess,
        error: handleFormError
    })

})

// this script is for downvoting
$('.downvote-btn-mobile').click(function(event){

    event.preventDefault();
    var button = $(event.target); // Button that triggered the modal
    var vote = $(this);
    var current_class_obj = vote.parent().parent();
    var current_class = current_class_obj.attr('current_class');
    var object = button.data('object');
    var dislike_url = button.data('href');

    if (dislike_url == '#'){
        return;
    }

    vote.parent().removeClass(current_class + '-mobile');  // removes whatever the current class is

    if(current_class == "unvoted"){
        // the class is not dislikes

        vote.parent().addClass('dislikes-mobile');  // adds the likes class
        current_class_obj.attr('current_class', 'dislikes');
        button.removeClass('down');
        button.addClass('downmod');


    } else if (current_class == 'likes'){

        other_vote_button = vote.parent().find('.arrow.upmod');
        other_vote_button.removeClass('upmod');
        other_vote_button.addClass('up');

        vote.parent().addClass('dislikes-mobile');  // adds the likes class
        current_class_obj.attr('current_class', 'dislikes');
        button.removeClass('down');
        button.addClass('downmod');

    } else {
        // the class is dislikes, so un-dislike

        vote.parent().addClass("unvoted-mobile");  // adds the unvoted class
        current_class_obj.attr('current_class', 'unvoted');

        if(button.hasClass('downmod')){
            button.removeClass('downmod');
            button.addClass('down');
        }
    }

    $.ajax({
        url: dislike_url,
        method: "GET",
        data: {},
        success: handleFormSuccess,
        error: handleFormError
    })

})
