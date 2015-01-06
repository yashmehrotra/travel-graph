function submit() {

    var email      = $('#email').val();
    var password   = $('#password').val();
    var first_name = $('#first_name').val();
    var last_name  = $('#last_name').val();

    $.ajax({
        type: "POST",
        url: "api/signup",
        data: {
            'email':email,
            'password':password,
            'first_name':first_name,
            'last_name':last_name,
        },
        success: function(result) {
            if(result) {
                console.log(result);
                // result = JSON.parse(result);
                // console.log(result['status']);
                // console.log(result.message);
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}