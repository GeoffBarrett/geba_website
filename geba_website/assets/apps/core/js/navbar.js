var browser = function() {
    // Return cached result if available, else get result then cache it.
    if (browser.prototype._cachedResult) {
        return browser.prototype._cachedResult;
    }

    // Opera 8.0+
    var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

    // Firefox 1.0+
    var isFirefox = typeof InstallTrigger !== 'undefined';

    // Safari 3.0+ "[object HTMLElementConstructor]"
    var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));

    // Internet Explorer 6-11
    var isIE = /*@cc_on!@*/false || !!document.documentMode;

    // Edge 20+
    var isEdge = !isIE && !!window.StyleMedia;

    // Chrome 1 - 71
    //var isChrome = !!window.chrome && (!!window.chrome.webstore || !!window.chrome.runtime); // this worked on stackOF but not locally...
    //var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor); // this is not specific to chrome
    var isChrome = ((navigator.userAgent.toLowerCase().indexOf('chrome') > -1) &&(navigator.vendor.toLowerCase().indexOf("google") > -1));

    // Blink engine detection
    var isBlink = (isChrome || isOpera) && !!window.CSS;

    return browser.prototype._cachedResult =
        isOpera ? 'Opera' :
        isFirefox ? 'Firefox' :
        isSafari ? 'Safari' :
        isChrome ? 'Chrome' :
        isIE ? 'IE' :
        isEdge ? 'Edge' :
        isBlink ? 'Blink':
        'Unknown'
};


$( document ).ready(function() {

    var currentBrowser = browser();

    if (currentBrowser == 'IE') {
        $('#mainNav').addClass('NoBrand');
        $('#mobile-nav').addClass('NoBrand');
    }

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

// this will search for whatever is searched for
$("#header-search-button").off("click").click(function(){
    $(this).hasClass("btn-primary")?($(this).removeClass("btn-primary"),
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
                return $("#header-search").submit(),
                !1
        })
        ,setTimeout(function(){
            $("#header-search-query").focus()},100))
})


// this will change the search type to the chosen value from the drop-down menu
$("#header-search-type a").click(function(){
    var dtype = $(this).attr("data-type");
    if(dtype.includes("all")){
        $("#header-search").attr("action","/search/");
    }
    else if (dtype.includes("project")){
        $("#header-search").attr("action","/project/search/");
    } else {
        $("#header-search").attr("action", "/" + dtype + "/");
    }
    $("#header-search-type .dropdown-toggle .title").html($(this).html()+" "),
    $("#header-search").hasClass("open")&&$("#header-search-query").select()
}),
$("#header-search").attr("action","/search/"); // this will set the action="/search"

var t=$("#search-type");

$("#header-search").submit(function(t){
    var e=$(this).attr("action"),a=$(this).find("input[name=query]").val();
    console.log(e);
    redirect(e+"?"+$.param({
        query:a
    })
    ),t.preventDefault()
})

$("#header-search-button").dblclick(function(){
    $(this).hasClass("open")||$(this).closest("form").submit()
})

redirect=function(t){
    window.Turbolinks&&Turbolinks.supported?Turbolinks.visit(t):window.location.href=t
}

showLoading=function(t){
    $("#loading-bg").show(),
    $("#loading-bg .loading-message").html(t),
    setTimeout(function(){
        $("#loading-bg").addClass("show")},50)
}

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