 // this script is to toggle the reply comments
$(".comment-reply-btn").click(function(event){
    event.preventDefault();
    console.log("hi");
    $(this).parent().parent().next(".comment-reply").fadeToggle();
})

// this script is to toggle the markdown help
$(".markdown-help-btn").click(function(event){
    event.preventDefault(); // prevents button from going to target
    $(this).next(".markdown-help").fadeToggle();
})


// this script is for deleting comments
$('#DeleteCommentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var content = button.data('content') // extract the content of the comment
    var modal = $(this)
    // var slug = button.data('slug'); // extract the slug of the comment
    var url = 'action="' + button.data('url') + '">'; // extra the url information
    //var csrf = button.data('csrf');
    var csrf = getCookie('csrftoken');

    modal.find('.modal-title').text('Delete Comment!')

    modal.find('.modal-body ').text('Do you want to delete the following comment:\n' + content + "!")

    modal.find('.modal-footer ').html(
    '<form method="POST" ' + url +
    '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf + '">' +
    '<button type="button submit" class="btn btn-primary modal_btn">Delete</button>' +
    '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>' +
    '</form>')
})