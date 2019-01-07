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

$("#menu-toggle").click( function (e){
    e.preventDefault();
    var sidebar_wrapper = $(document.getElementById('sidebar-wrapper'));
    var content_wrapper = $(document.getElementById('page-content-wrapper'));
    var menu_btn = $(document.getElementById('menu-toggle'));

    sidebar_wrapper.toggleClass("menuDisplayed");
    content_wrapper.toggleClass("menuDisplayed");
    menu_btn.toggleClass("menuDisplayed");
});


(function($) {
  "use strict"; // Start of use strict

  // Show the navbar when the page is scrolled up
  var MQL = 1170;

  //primary navigation slide-in effect
  if ($(window).width() > MQL) {
    var headerHeight = $('#mainNav').height();
    $(window).on('scroll', {
        previousTop: 0
      },
      function() {
        var currentTop = $(window).scrollTop();
        //check if user is scrolling up

        if (currentTop < this.previousTop) {
          $('#mainNav').removeClass('open');
          $('#mobile-nav').removeClass('open');
          $('#mobile-nav-button').removeClass('open');
          //if scrolling up...
          if (currentTop > 0 && $('#mainNav').hasClass('is-fixed')) {
            $('#mainNav').addClass('is-visible');
          } else {
            $('#mainNav').removeClass('is-visible is-fixed');
          }
        } else if (currentTop > this.previousTop) {
          //if scrolling down...
          $('#mainNav').removeClass('open');
          $('#mobile-nav').removeClass('open');
          $('#mobile-nav-button').removeClass('open');
          $('#mainNav').removeClass('is-visible');
          if (currentTop > headerHeight && !$('#mainNav').hasClass('is-fixed')) $('#mainNav').addClass('is-fixed');
        }
        this.previousTop = currentTop;
      });
  }

})(jQuery); // End of use strict