// this script is for deleting comments
$('#DeleteProjectModalIndex').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var content = button.data('content') // extract the content of the comment
    var modal = $(this)
    // var slug = button.data('slug'); // extract the slug of the comment
    var url = 'action="' + button.data('url') + '">'; // extra the url information
    var csrf = getCookie('csrftoken');

    modal.find('.modal-title').text('Delete Project!')

    modal.find('.modal-body ').text('Do you want to delete the following Project:\n\n ' + content + "?")

    modal.find('.modal-footer ').html(
    '<form method="POST" ' + url +
    '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf + '">' +
    '<button type="button submit" class="btn btn-primary modal_btn">Delete</button>' +
    '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>' +
    '</form>')
})

$('#DeleteProjectPostModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var content = button.data('content') // extract the content of the comment
    var modal = $(this)
    // var slug = button.data('slug'); // extract the slug of the comment
    var url = 'action="' + button.data('url') + '">'; // extra the url information
    var csrf = getCookie('csrftoken');

    modal.find('.modal-title').text('Delete Post!')

    modal.find('.modal-body ').text('Do you want to delete the following Project Post:\n\n ' + content + "?")

    modal.find('.modal-footer ').html(
    '<form method="POST" ' + url +
    '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf + '">' +
    '<button type="button submit" class="btn btn-primary modal_btn">Delete</button>' +
    '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>' +
    '</form>')
})

// this will set the search option and value so that it defaults to searching with the projects option
$( document ).ready(function() {
    $("#header-search").attr("action","/project/search/"); // this will set the action="/search"
    $("#header-search-type .dropdown-toggle .title").html('Projects ');
});