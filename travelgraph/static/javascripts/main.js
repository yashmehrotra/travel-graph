// Necessary for POST Requests to work!
var app = angular.module('travelGraph', ['ngStorage', 'ngFacebook'], function($httpProvider) {
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


app.run(['$rootScope', '$location', '$localStorage', 'AuthService', function ($rootScope, $location, $localStorage, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event) {
    if ($localStorage.isLoggedIn == true) {
      console.log('ALLOW');
    } else {
	console.log('DENY');
	var path = $location.path();
	if (path == "/login" || path == "/signup" || path == "/") {
	  // console.log("Allowed for the current location");
	} else {
	  event.preventDefault();
	  $location.path('/login');  // Redirect to login page
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
        ck.destroy(false);
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
      })
      .when('/login', {
	templateUrl: '/static/partials/login.html',
      })
      .when('/signup', {
	templateUrl: '/static/partials/signup.html',
      })
      .when('/ques/:quesId', {
	templateUrl: '/static/partials/QnA.html',
	controller: 'QuestionController'
      })
      .when('/question', {
	templateUrl: '/static/partials/question.html',
	controller: 'AddQuestionController'
      })
      .when('/all_questions', {
	templateUrl: '/static/partials/all_questions.html',
	controller: 'AllQuestionsController'
      })
      .otherwise({
	redirectTo: '/'
      });
    $locationProvider.html5Mode(true);
  }]);

// Filter for displaying posts in the reverse order (latest first)
app.filter('reverse', function() {
  return function(items) {
    return items.slice().reverse();
  };
});

// Factory service for user login/logout updations..
app.factory( 'AuthService', function($http, $compile) {
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

// Application-wide controller [Handles all login/logout & new user stuff]
app.controller('MainController', ['$scope', '$http', 'AuthService', '$location', '$localStorage', '$facebook', function ($scope, $http, AuthService, $location, $localStorage, $facebook) {

  var DEFAULT_USER_AVATAR = "/static/images/placeholder_avatar.svg";

  $scope.newUserDetails = {};
  $scope.userData = {};
  $scope.loginDetails = {};
  $scope.currentUserData = {};
  $scope.invalidCredentials = false;
  $scope.loginData = {};
  
  // Update this wherever login/logout is done.. use $watch/$on etc in future..
  $scope.loggedIn = false;

  // if the user credentials are already stored in localstorage..
  if (typeof($localStorage.isLoggedIn) != 'undefined' && $localStorage.isLoggedIn == true) {
    $scope.loggedIn = $localStorage.isLoggedIn;
    $scope.userData.user_id = $localStorage.user_auth.user_id;
    $scope.userData.username_id = $localStorage.user_auth.username_id;
    $scope.userData.first_name = $localStorage.user_auth.first_name;
    $scope.userData.last_name_id = $localStorage.user_auth.last_name_id;
    $scope.userData.email_ = $localStorage.user_auth.email;
    $scope.userData.profile_photo = $localStorage.user_auth.profile_photo;
  }

  /**
   * Functions for login/logout through email or Facebook..
   */
  $scope.loginUser = function(loginDetails) {
    $scope.invalidCredentials = false;
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
	if (response.status == 'success') {
	  $scope.currentUserData.userName = response.username;
	  AuthService.setUser(response);
	} else {
	  $scope.invalidCredentials = true;
	}
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  };

  $scope.FbLogin = function() {
    console.log("Inside Fblogin Function");
    $facebook.login().then(function() {
      $facebook.api("/me", {'fields':'picture,id,email,first_name,last_name'}).then(
	function(response) {
	  var data = {
	    email: response.email,
	    first_name: response.first_name,
	    last_name: response.last_name,
	    profile_photo: response.picture.data.url,
	    method: "facebook"
	  };
	  $http({
	    method: 'POST',
	    url: '/api/signup',
	    data: data
	  })
	    .success(function(response, status){
	      $scope.loginAfterFb(data);
	    }).error(function(response, status){
	      console.log("Request Failed");
	    });
	}
      );
    });
  };

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
	if (response.status == 'success') {
	  AuthService.setUser(response);
	}
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  };

  $scope.logoutUser = function (){
    $http({
      method: 'GET',
      url: '/api/logout'
    })
      .success(function(data, status){
	AuthService.setUser(false);
	$localStorage.$reset({
	  isLoggedIn: false
	});
	$scope.loggedIn = $localStorage.isLoggedIn;
	$location.path('/'); // Redirect to main page...
      })
      .error(function(data, status){
	console.log("Request Failed");	
      });
  };

  $scope.addUser = function(loginData) {
    $scope.invalidCredentials = false;
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
    $http({
      method: 'POST',
      url: '/api/signup',
      data: data
    })
      .success(function(response, status){
	if(response.status == "success") { 
	  $scope.loginUser(data);	// login as soon as a user signs up....
	} else {
	  $scope.invalidCredentials = true;
	}
      }).error(function(response, status){
	console.log("Request Failed");
      });
  };

  // watch for user login.. 
  $scope.$watch(AuthService.isLoggedIn, function (value, oldValue) {
    // As soon as the user logs in..
    // Can we make it a general function - called when logged in, followed someone etc.
    if(value) {
      console.log("Connect");
      $localStorage.isLoggedIn = true;
      $scope.loggedIn = $localStorage.isLoggedIn;
      data_user = AuthService.isLoggedIn();
	
      // Fetch the user details
      $http({
        method: 'GET',
        url: '/api/user/' + data_user.user_id + '/'
      })
        .success(function(response, status){
	  var storageData = {
	    'user_id': response.user_id,
	    'username': response.username,
	    'first_name': response.first_name,
	    'last_name': response.last_name,
	    'email': response.email,
	    'profile_photo': response.profile_photo
        // Do response.user_followers, response.user_following
	  };
	  $localStorage.user_auth = storageData; // Store the user auth info in localstorage
	  $scope.userData = storageData;
        })
        .error(function(response, status){
          console.log("Request Failed");
      });

      // Fetch the list of users the user is following
      $http({
        method: 'GET',
        url: '/api/user_follow/'
      })
        .success(function(response, status){
	  $localStorage.users_followed = response; // Fetch the list of users the current user is following
	})
        .error(function(response, status){
          console.log("Request Failed");
      });

      // Fetch the list of questions the user has subscribed to..
      $http({
        method: 'GET',
        url: '/api/user/follow_question'
      })
        .success(function(response, status){
	  $localStorage.questions_subscribed = response; // Fetch the list of users the current user is following
	  $location.path('/all_questions'); // Redirect once logged in...
        })
        .error(function(response, status){
          console.log("Request Failed");
      });
	
    }
  }, true);
}]);

// For displaying a question and answers page
app.controller('QuestionController', function QuestionController($route, $scope, $http, AuthService, $localStorage, $routeParams, $route) {
  $scope.questionData = {};
  $scope.askerDetails = {};
  $scope.answerData = [];
  $scope.answerCount = 0;
  $scope.postAnswerData = {};
  $scope.postAnswerData.tags = "";
  $scope.currentUserId = $localStorage.user_auth.user_id;
  $scope.questionData.questionId = $routeParams.quesId;  // Fetch the question_id details from route

  $scope.followsUser = false; // check default values
  $scope.subscribedQuestion = false; // check default values
    
  // Fetch the current question details
  var request_url = '/api/content/get_question/' + $scope.questionData.questionId + "/";
  $http({
    method: 'GET',
    url: request_url,
  })
    .success(function(response, status){
      $scope.questionData.questionText = response.question_text;
      $scope.questionData.questionDescription = response.question_desc;
      $scope.questionData.questionTags = response.question_tags;
      $scope.askerDetails.userId = response.user_id;
      $scope.getAskerData();
      $scope.getAnswers();
    })
    .error(function(response, status){
      console.log("Request Failed");
    });
  
  // Fetch the asker details from the user id..
  $scope.getAskerData = function(){
    var request_url = '/api/user/' + $scope.askerDetails.userId + '/';
    $http({
      method: 'GET',
      url: request_url,
    })
      .success(function(response, status){
	$scope.askerDetails.name = response.first_name + " " + response.last_name;
	$scope.askerDetails.profilePhoto = response.profile_photo;
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  };

  // If the current user is following the asker
  if($localStorage.users_followed.indexOf($scope.askerDetails.userId) != -1) {
    $scope.followsUser = true;
  }
  // If the current user has subscribed to this question
  if($localStorage.questions_subscribed.indexOf($scope.questionData.questionId) != -1) {
    $scope.subscribedQuestion = true;
  }
    
  // Post an answer
  $scope.postAnswer = function() {
    var data = {
      question_id: $scope.questionData.questionId,
      answer: $scope.postAnswerData.text,
      answer_tags: $scope.postAnswerData.tags,
      user_id: $scope.currentUserId,
    };
    console.log(data);
    $http({
      method: 'POST',
      url: '/api/content/add_answer',
      data: data
    })
      .success(function(response, status){
	// Instead of reloading, ng-repeat should automatically update the dom
	$route.reload();  // Reload once the user posts an answer..
      })
      .error(function(response, status){
    	console.log("Request Failed");
    });
  };

  // Get the answers to the current question
  $scope.getAnswers = function(){
    var request_url = '/api/content/get_answers/' + $scope.questionData.questionId + '/'; 
    $http({
      method: 'GET',
      url: request_url,
    })
      .success(function(response, status){
	if (response.answers.length == 0) {
	  // $scope.answersData = "No answers to display";
	} else {
	  $scope.answerData = response.answers;
	  $scope.answerCount = $scope.answerData.length;
	}
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  };
    
  // Follow another user..
  $scope.followAsker = function(){
    var request_url = '/api/user_follow/';
    var data = {
      'user_id': $localStorage.user_auth.user_id,
      'follow_id': $scope.askerDetails.userId
    };
    $http({
      method: 'POST',
      url: request_url,
      data: data
    })
      .success(function(response, status){
	// change button state.. ng-switch	
      })
      .error(function(response, status){
    	console.log("Request Failed");
    });
  }
});

// Ask a question
app.controller('AddQuestionController', function AddQuestionController($scope, $http, $location){
  $scope.questionData = {};

  $scope.postQuestion = function() {
    var request_url = '/api/content/add_question';
    var data = {
      question_title: $scope.questionData.title, 
      question_desc: $scope.questionData.description,
      question_tags: $scope.questionData.tags
    };
    $http({
      method: 'POST',
      url: request_url,
      data: data
    })
      .success(function(response, status){
	$location.path('/all_questions');
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  };

});

// List all questions
app.controller('AllQuestionsController', function AllQuestionsController($scope, $http, $location){
  $scope.questionsList = [];
  
  // Fetch the list of all questions..
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

  $scope.goToQuestion = function(question_id) {
    var redirect_to_url = '/ques/' + question_id;
    $location.path(redirect_to_url); // Redirect to the question's page
  };

});
