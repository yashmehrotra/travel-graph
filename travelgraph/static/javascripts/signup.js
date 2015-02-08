function post_to_api(email, password, first_name, last_name, method) {

    $.ajax({
        type: "POST",
        url: "api/signup",
        data: {
            'email':email,
            'password':password,
            'first_name':first_name,
            'last_name':last_name,
            'method':method,
        },
        success: function(result) {
            if(result) {
                console.log(result);
                // result = JSON.parse(result);
                // console.log(result['status']);
                // console.log(result.message);
            } else {
                console.log('Problem with ajax'); //1423273901281785
            }
        }
    });
}

function submit() {
    var email      = $('#email').val();
    var password   = $('#password').val();
    var first_name = $('#first_name').val();
    var last_name  = $('#last_name').val();
    var method     = 'normal';
    console.log(email,password,first_name);

    post_to_api(email, password, first_name, last_name, method);
}


// Facebook
function statusChangeCallback_b(response) {
    console.log('statusChangeCallback');
    
    if (response.status === 'connected') {
        console.log('Below');
        FB.api('/me', function(response) {
            console.log(response)
            console.log('Successful login for: ' + response.name);
            // Generate a complicated password and put this in a different func
            var method = 'facebook';
            post_to_api(response.email, '123456', response.first_name, response.last_name, method)
        });
    } else if (response.status === 'not_authorized') {
        console.log('log into app')
    } else {
        console.log('log into facebook')
    }
}

function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    
    if (response.status === 'connected') {
        console.log('Below');
        FB.api('/me', function(response) {
            console.log(response)
            
        });
    } else if (response.status === 'not_authorized') {
        console.log('log into app')
    } else {
        console.log('log into facebook')
    }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
        //button
        statusChangeCallback_b(response);
    });
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '1423273901281785',
        cookie     : true,  // enable cookies to allow the server to access 
                        // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.1' // use version 2.1
    });

    FB.getLoginStatus(function(response) {
        console.log(response.name);
        statusChangeCallback(response);
    });

};

// Load the SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
