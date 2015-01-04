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
                result = JSON.parse(result);
                console.log(result['status']);
                console.log(result.message);
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}