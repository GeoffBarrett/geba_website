// this will set the search option and value so that it defaults to searching with the All option
$( document ).ready(function() {
    $("#header-search").attr("action","/search/"); // this will set the action="/search"
    $("#header-search-type .dropdown-toggle .title").html('All ');
});

$(document).ready(function() {

  if(window.location.href.indexOf('#contact_sent') != -1) {
    $('#contact_sent').modal('show');
  }

});