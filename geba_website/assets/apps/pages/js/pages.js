// this will set the search option and value so that it defaults to searching with the All option
$( document ).ready(function() {
    $("#header-search").attr("action","/search/"); // this will set the action="/search"
    $("#header-search-type .dropdown-toggle .title").html('All ');
});