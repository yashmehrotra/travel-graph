$(function(){
  $('#login-button').on('click', submit);
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
                result = JSON.parse(result);
                console.log(result['status']);
                console.log(result.message);
		window.location.href = "http://localhost:5000/ques/1";
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}