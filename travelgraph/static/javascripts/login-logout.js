$(function(){
  $('#header-logout').on('click', logout_user);
});

function logout_user() {
  $.ajax({
    type: "GET",
    url: "/api/logout",
    success: function() {
      // Redirect to login/homepage
    }
  });  
}