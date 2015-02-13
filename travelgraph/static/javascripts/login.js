$(function(){
  $('#login-button').on('click', submit);
  
  // DEBUG THIS...
  $('.login-input').on('keypress', function(event){
    event.preventDefault();
    if (event.which == 13) {
      // alert("Hello");
      submit();
    }
  });

});


function submit() {
    var email = $('#email').val();
    var password = $('#password').val();

    $.ajax({
        type: "POST",
        url: "api/login",
        data: {
            'email':email,
            'password':password,
        },
        success: function(result) {
            if(result) {
                console.log(result);
                console.log(result['status']);
                console.log(result.message);
		window.location.href = "/ques/1";
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}