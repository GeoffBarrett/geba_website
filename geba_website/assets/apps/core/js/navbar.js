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


$("#header-search-button").off("click").click(function(){

   $(this).hasClass("btn-primary")?($(this).removeClass("btn-primary"),
   $("#header-shop").removeClass("search-open"),
   $("#header-search").removeClass("open"),
   $("#header-search-type").removeClass("shown"),
   $("#header-search-query").removeClass("open")):
       ($(this).addClass("btn-primary"),
       $("#header-search").addClass("open"),
       $("#header-search-type").addClass("shown"),
       $("#header-search-query").addClass("open").keypress(function(t){
           if(t=t||window.event,27==t.keyCode)
               $(this).removeClass("open").blur(),
               $("#header-search-button").removeClass("btn-primary"),
               $("#header-search-type").removeClass("shown");
           else if(13==t.keyCode)
               return
               $("#header-search").submit(),
               !1
           }),
           setTimeout(function(){$("#header-search-query").focus()}))
})

$("#mobile-nav-button").click(function(t){
    return t.preventDefault(),
	$(this).hasClass("open")?($(this).removeClass("open"),
	$("#mainNav").removeClass("open"),
	$("#mobile-nav").removeClass("open"),
	$("#mobile-user-nav").removeClass("open"),
	$("#mobile-user-avatar").removeClass("open")):(
	$(this).addClass("open"),
	$("#mainNav").addClass("open"),
	$("#mobile-nav").addClass("open"),
	$("#mobile-user-nav").removeClass("open"),
	$("#mobile-user-avatar").removeClass("open")),
	!1
})


$("#mobile-user-avatar").click(function(t){
    return t.preventDefault(),
	$(this).hasClass("open")?($(this).removeClass("open"),
	$("#mainNav").removeClass("open"),
	$("#mobile-nav").removeClass("open"),
	$("#mobile-user-nav").removeClass("open"),
	$("#mobile-user-avatar").removeClass("open")):(
	$(this).addClass("open"),
	$("#mainNav").addClass("open"),
	$("#mobile-nav").removeClass("open"),
	$("#mobile-user-nav").addClass("open"),
	$("#mobile-user-avatar").addClass("open")),
	!1
})