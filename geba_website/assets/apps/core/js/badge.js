$('.publish-btn').click(function(event){

    event.preventDefault();

    var button = $(event.target); // Button that triggered the modal

    var slug = button.data('slug');

    var draft_badge = $("span#draft-" + slug);

    var draft_btn = $(document.getElementById("draft_" + slug));

    var publish_url = button.data('href');

    if (publish_url == '#'){
        return;
    }

    if (!button.hasClass('hidebtn')){
        button.addClass('hidebtn');
    }

    if (draft_btn.hasClass('hidebtn')){
        draft_btn.removeClass('hidebtn');
    }

    if (!draft_badge.hasClass('hidebadge')){
        draft_badge.addClass('hidebadge');
    }

    $.ajax({
        url: publish_url,
        method: "GET",
        data: {},
        success: function(data){
            console.log(data)},
        error: function(error){
            console.log(error)
            if (error.indexOf("Authentication") !== -1){
                console.log("Authenticate!")
            }
            console.log("error")
        }
    })

})

$('.draft-btn').click(function(event){

    event.preventDefault();

    var button = $(event.target); // Button that triggered the modal

    var slug = button.data('slug');

    var draft_badge = $("span#draft-" + slug);

    var publish_btn = $(document.getElementById("publish_" + slug));

    var draft_url = button.data('href');

    if (draft_url == '#'){
        return;
    }

    if (!button.hasClass('hidebtn')){
        button.addClass('hidebtn');
    }

    if (publish_btn.hasClass('hidebtn')){
        publish_btn.removeClass('hidebtn');
    }

    if (draft_badge.hasClass('hidebadge')){
        draft_badge.removeClass('hidebadge');
    }

    $.ajax({
        url: draft_url,
        method: "GET",
        data: {},
        success: function(data){
            console.log(data)},
        error: function(error){
            console.log(error)
            if (error.indexOf("Authentication") !== -1){
                console.log("Authenticate!")
            }
            console.log("error")
        }
    })

})