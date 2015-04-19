// Necessary for POST Requests to work!
var app = angular.module('travel-graph', ['ngCookies', 'ngFacebook'], function($httpProvider) {
  // Use x-www-form-urlencoded Content-Type
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

  /**
   * The workhorse; converts an object to x-www-form-urlencoded serialization.
   * @param {Object} obj
   * @return {String}
   */ 
  var param = function(obj) {
    var query = '', name, value, fullSubName, subName, subValue, innerObj, i;
      
    for(name in obj) {
      value = obj[name];
        
      if(value instanceof Array) {
        for(i=0; i<value.length; ++i) {
          subValue = value[i];
          fullSubName = name + '[' + i + ']';
          innerObj = {};
          innerObj[fullSubName] = subValue;
          query += param(innerObj) + '&';
        }
      }
      else if(value instanceof Object) {
        for(subName in value) {
          subValue = value[subName];
          fullSubName = name + '[' + subName + ']';
          innerObj = {};
          innerObj[fullSubName] = subValue;
          query += param(innerObj) + '&';
        }
      }
      else if(value !== undefined && value !== null)
        query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
    }
      
    return query.length ? query.substr(0, query.length - 1) : query;
  };

  // Override $http service's default transformRequest
  $httpProvider.defaults.transformRequest = [function(data) {
    return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
  }];
});


app.config( function( $facebookProvider ) {
  $facebookProvider.setAppId('1423273901281785');
});


app.run(['$route', function($route)  {
  $route.reload();
}]);


app.run(['$rootScope', '$location', '$cookieStore', 'AuthService', function ($rootScope, $location, $cookieStore, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event) {
    if ($cookieStore.get('user_auth')) {
      console.log('ALLOW');
      console.log($cookieStore.get('user_auth'));
    } else {
	console.log('DENY');
	var path = $location.path();
	if (path == "/login" || path == "/signup" || path == "/") {
	  console.log("Allowed");
	} else {
	  event.preventDefault();
	  $location.path('/login'); 
	}
      }
    });
}]);

app.run( function( $rootScope ) {
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));  
});

// For ckeditor integration in AngularJS
app.directive('ckEditor', [function () {
  return {
    require: '?ngModel',
    restrict: 'C',
    link: function (scope, elm, attr, model) {
      var isReady = false;
      var data = [];
      var ck = CKEDITOR.replace(elm[0]);
      
      function setData() {
        if (!data.length) {
          return;
        }
        
        var d = data.splice(0, 1);
        ck.setData(d[0] || '<span></span>', function () {
          setData();
          isReady = true;
        });
      }

      ck.on('instanceReady', function (e) {
        if (model) {
          setData();
        }
      });
      
      elm.bind('$destroy', function () {
        // ck.destroy(false);
      });

      if (model) {
        ck.on('change', function () {
          scope.$apply(function () {
            var data = ck.getData();
            if (data == '<span></span>') {
              data = null;
            }
            model.$setViewValue(data);
          });
        });

        model.$render = function (value) {
          if (model.$viewValue === undefined) {
            model.$setViewValue(null);
            model.$viewValue = null;
          }

          data.push(model.$viewValue);

          if (isReady) {
            isReady = false;
            setData();
          }
        };
      }
      
    }
  };
}]);


// Prevent conflict with Flask!
app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
	templateUrl: '/static/partials/home.html',
	// controller: 'MainCtrl'
      })
      .when('/login', {
	templateUrl: '/static/partials/login.html',
	controller: 'MainCtrl'
      })
      .when('/ques/:quesId', {
	templateUrl: '/static/partials/QnA.html',
	controller: 'QuestionCtrl'
      })
      .when('/signup', {
	templateUrl: '/static/partials/signup.html',
	controller: 'NewUserCtrl'
      })
      .when('/question', {
	templateUrl: '/static/partials/question.html',
	controller: 'AddQuestionCtrl'
      })
      .when('/all_questions', {
	templateUrl: '/static/partials/all_questions.html',
	controller: 'AllQuestionsCtrl'
      })
      // .when('/home', {
      // 	templateUrl: '/static/partials/home.html'
      // 	// controller: 'HomeCtrl'
      // })
      .otherwise({
	redirectTo: '/'
      })
    ;
    $locationProvider.html5Mode(true);
  }]);


app.factory( 'AuthService', function($http) {
  var user;

  return {
    setUser : function(aUser){
        user = aUser;
    },
    isLoggedIn : function(){
        return(user)? user : false;
    }
  };

});

app.factory( 'CurrentQuestionService', function($http) {
  var currentQuestionData;

  return {
    setData : function(data){
      currentQuestionData = data;
    },
    getData : function(){
      return(currentQuestionData)? currentQuestionData : false;
    }
  };

});

// not in actual use currently
app.factory( 'AllQuestionsService', function($http) {
  var allQuestionsData;

  return {
    setData : function(data){
      allQuestionsData = data;
    },
    getData : function(){
      return(allQuestionsData)? allQuestionsData : false;
    }
  };

});


// Needs Debugging ..
app.controller('MainCtrl', ['$scope', '$http', 'AuthService', 'CurrentQuestionService', 'AllQuestionsService', '$location', '$cookieStore', '$facebook', function ($scope, $http, AuthService, CurrentQuestionService, AllQuestionsService, $location, $cookieStore, $facebook) {

  $scope.$watch(AuthService.isLoggedIn, function (value, oldValue) {

    if(!value && oldValue) {
      console.log("Disconnect");
      $cookieStore.put('user_auth', false);
      $location.path('/');
    }
    
    // As soon as the user logs in..
    if(value) {
      console.log("Connect");
      data_user = AuthService.isLoggedIn();

      $http({
        method: 'GET',
        url: '/api/user/' + data_user.user_id + '/'
      })
        .success(function(response, status){
	  console.log(response);
	  var cookieData = {
	    'user_id': response.user_id,
	    'username': response.username,
	    'first_name': response.first_name,
	    'last_name': response.last_name,
	    'email': response.email,
	    'profile_photo': response.profile_photo
	  }
	  $cookieStore.put('user_auth', cookieData);
        })
        .error(function(response, status){
          console.log("Request Failed");
      });
      // Redirect user once logged in..
      $location.path('/all_questions');
    }

  }, true);

  $scope.FbLogin = function() {
    console.log("FB login function");
    $facebook.login().then(function() {
      console.log('Logged in with FB');
      $facebook.api("/me", {'fields':'picture,id,email,first_name,last_name'}).then(
	function(response) {
	  console.log(response);
	  var data = {
	    email: response.email,
	    first_name: response.first_name,
	    last_name: response.last_name,
	    profile_photo: response.picture.data.url,
	    method: "facebook"
	  };

	  console.log(data);

	  $http({
	    method: 'POST',
	    url: '/api/signup',
	    data: data
	  })
	    .success(function(response, status){
	      console.log("Signup with FB success!");
	      console.log(response);
	      console.log("User exists fb");
	      $scope.loginAfterFb(data);
	    }).error(function(response, status){
	      console.log("Request Failed");
	    });
	}

      );
    });
  }

  $scope.loginAfterFb = function(data) {
      
    var data = {
      email: data.email,
      method: 'facebook'
    };
    
    $http({
      method: 'POST',
      url: '/api/login',
      data: data
    })
      .success(function(response, status){
	console.log("Success:", response);
	if (response.status == 'success') {
	  console.log(response);
	  AuthService.setUser(response);
	}
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
	
  }

}]);


app.filter('reverse', function() {
  return function(items) {
    return items.slice().reverse();
  };
});

// For user login and logout
  app.controller('LoginLogoutCtrl', ['$scope', '$http', 'AuthService', function LoginLogoutCtrl($scope, $http, AuthService, NewUserCtrl, $cookieStore){

  $scope.loginDetails = {};
  $scope.currentUserData = {};
  $scope.invalidCredentials = false;
  $scope.loginData = {};

  $scope.loginUser = function(loginDetails) {
    var data = {
      email: loginDetails.email,
      password: loginDetails.password,
      method: 'normal'
    };
    $http({
      method: 'POST',
      url: '/api/login',
      data: data
    })
      .success(function(response, status){
	console.log("Success:", response);
	if (response.status != 'failed') {
	  $scope.currentUserData.userName = response.username;
	  console.log(response);
	  AuthService.setUser(response);
	} else {
	  console.log("Invalid credentials");
	  $scope.invalidCredentials = true;
	  // invalid_credentials();
	}
      })
      .error(function(response, status){
	console.log("Request Failed");
	// function Invalid_credentials() {
	// }
      });
  };
  
   // $scope.fbLogin = function(){
     // console.log("FB login function");
     // $facebook.login().then(function() {
     //   console.log('Logged in with FB');
     // });
  //   // Here we run a very simple test of the Graph API after login is
  //   // successful.  See statusChangeCallback() for when this call is made.
  //   function testAPI() {
  //     console.log('Welcome!  Fetching your information.... ');
  //     FB.api('/me',{'fields':'picture,id,first_name,email,last_name'}, function(response) {
  // 	console.log('Successful login for: ' + response.name);      
  // 	console.log(response);
  // 	$scope.loginData = response;
  // 	$scope.loginData.method = 'facebook';
  // 	NewUserCtrl.addUser($scope.loginData);
  // 	$scope.loginUser($scope.loginData);
  //     });
  //   }

  // };

  // $scope.me = function() {
  //   // Facebook.api('/me', function(response) {
  //   //   $scope.user = response;
  //   // });
  // };

  $scope.logoutUser = function (){
    $http({
      method: 'GET',
      url: '/api/logout'
    })
      .success(function(data, status){
	console.log("Successfully Logged out!");
	AuthService.setUser(false);
      })
      .error(function(data, status){
	console.log("Request Failed");	
      });
    // console.log(AuthService.isLoggedIn());
  };

}]);

// For displaying a question and answer page
app.controller('QuestionCtrl', function QuestionCtrl($route, $scope, $http, CurrentQuestionService, AuthService, $cookieStore, $routeParams, $route) {
  $scope.questionData = {};
  $scope.askerDetails = {};
  $scope.answerData = [];
  $scope.answerCount;
  $scope.text = "";
  
  $scope.answerTags = "";
  
  // Fetch the question_id details from route
  var question_id = $routeParams.quesId;
  console.log("The Question id is:", question_id);

  // Fetch the question details from id
    $http({
      method: 'GET',
      url: '/api/content/get_question/' + question_id + "/"
    })
      .success(function(response, status){
      	console.log(response);
	$scope.questionData.questionId = question_id;
	$scope.questionData.questionText = response.question_text;
	$scope.questionData.questionDescription = response.question_desc;
	$scope.questionData.questionTags = response.question_tags;
	$scope.askerDetails.user_id = response.user_id;
	
	$http({
	  method: 'GET',
	  url: '/api/user/' + $scope.askerDetails.user_id + '/'
	})
	  .success(function(response, status){
	    $scope.askerDetails.name = response.first_name + " " + response.last_name;
	    // if (response.profile_photo === )
	    $scope.askerDetails.profile_photo = response.profile_photo;
	  })
	  .error(function(response, status){
	    console.log("Request Failed");
	  });
	
      })
      .error(function(response, status){
      	console.log("Request Failed");
      });


  $scope.postAnswer = function() {
    console.log($scope.text);
    console.log($scope.answerTags);
    var data = {
      question_id: question_id,
      answer: $scope.text,
      answer_tags: $scope.answerTags,
      user_id: $cookieStore.get('user_auth').user_id
    };
    $http({
      method: 'POST',
      url: '/api/content/add_answer',
      data: data
    })
      .success(function(response, status){
    	console.log("Success " , response);
	$route.reload();
      })
      .error(function(response, status){
    	console.log("Request Failed");
    });
  };

  // Get the answers to the current question
  $http({
    method: 'GET',
    url: '/api/content/get_answers/' + question_id + '/'
  })
    .success(function(response, status){
      if (response.answers.length == 0) {
	  $scope.answersData = "No answers to display";
      } else {
	console.log(response.answers[0].answer);
	$scope.answerData = response.answers;
	console.log($scope.answerData);
	$scope.answerCount = $scope.answerData.length;
	console.log($scope.answerCount);
      }
    })
    .error(function(response, status){
      console.log("Request Failed");
    });

})

// Signup page 
// app.controller('NewUserCtrl', function NewUserCtrl($scope, $http, $cookieStore, LoginLogoutCtrl) {
app.controller('NewUserCtrl', function NewUserCtrl($scope, $http, $cookieStore) {
  $scope.newUserDetails = {};
  var DEFAULT_USER_AVATAR = "/static/images/placeholder_avatar.svg";

  $scope.addUser = function(loginData) {
    var data = {
      email: $scope.newUserDetails.email,
      password: $scope.newUserDetails.password,
      first_name: $scope.newUserDetails.firstName,
      last_name: $scope.newUserDetails.lastName,
      profile_photo: "",
      method: "normal"
    };

    if (data.method == 'normal') {
      data.profile_photo = DEFAULT_USER_AVATAR;
    }
      
    console.log(data);

    $http({
      method: 'POST',
      url: '/api/signup',
      data: data
    })
      .success(function(response, status){
	console.log(response);
	// LoginLogoutCtrl.loginUser($scope.newUserDetails);
      }).error(function(response, status){
	console.log("Request Failed");
      });
  }
});

// Ask a question
app.controller('AddQuestionCtrl', function AddQuestionCtrl($scope, $http, $location){
  $scope.questionData = {};
  $scope.text = "";
  $scope.postQuestion = function() {
    var data = {
      question_title: $scope.questionData.title, 
      question_desc: $scope.text,
      question_tags: $scope.questionData.tags
    };
    console.log(data);
    $http({
      method: 'POST',
      url: '/api/content/add_question',
      data: data
    })
      .success(function(response, status){
	console.log(response);
	$location.path('/all_questions');
	console.log($scope.questionData.title);
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  }
});

// List all questions
app.controller('AllQuestionsCtrl', function AllQuestionsCtrl($scope, $http, CurrentQuestionService, $location){
  $scope.questionsList = [];
  $scope.goToQuestion = function(question_id) {
  
  console.log(question_id);

    // Fetch the question details from id
    $http({
      method: 'GET',
      url: '/api/content/get_question/' + question_id + "/"
    })
      .success(function(response, status){
      	console.log(response);
	
      	// Set current question data 
      	CurrentQuestionService.setData(response);
	
      	// Redirect to question page
      	$location.path('/ques/' + question_id);
      })
      .error(function(response, status){
      	console.log("Request Failed");
      });
 
  }
  $http({
    method: 'GET',
    url: '/api/content/view_all_ques'
  })
    .success(function(response, status){
      $scope.questionsList = response.questions;
      console.log($scope.questionsList);
    }).error(function(response, status){
      console.log("Request Failed");
    });

});