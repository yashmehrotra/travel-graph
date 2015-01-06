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

// Facebook
window.fbAsyncInit = function() {
    FB.init({
        appId      : '1423273901281785',
        xfbml      : true,
        version    : 'v2.2'
    });
};

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));