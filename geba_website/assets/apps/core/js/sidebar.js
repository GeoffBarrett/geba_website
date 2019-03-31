
$("#menu-toggle").click( function (e){
    e.preventDefault();
    var sidebar_wrapper = $(document.getElementById('sidebar-wrapper'));
    var content_wrapper = $(document.getElementById('page-content-wrapper'));
    var menu_btn = $(document.getElementById('menu-toggle'));

    sidebar_wrapper.toggleClass("menuDisplayed");
    content_wrapper.toggleClass("menuDisplayed");
    menu_btn.toggleClass("menuDisplayed");
});