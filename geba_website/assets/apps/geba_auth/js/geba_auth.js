$(document).ready(function() {

  if(window.location.href.indexOf('#activation_sent') != -1) {
    $('#activation_sent').modal('show');
  }

  if(window.location.href.indexOf('#reset_sent') != -1) {
    $('#reset_sent').modal('show');
  }

});