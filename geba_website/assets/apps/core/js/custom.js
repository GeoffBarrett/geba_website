$(document).ready(function(){
    $(".post-body img").each(function(){
        $(this).addClass("img-responsive");
    })
})

$(document).ready(function(){
    $(".project-body img").each(function(){
        $(this).addClass("img-responsive");
    })
})

$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });
});