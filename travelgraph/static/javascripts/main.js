// Necessary for POST Requests to work!
var app = angular.module('travel-graph', [], function($httpProvider) {
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

app.run(['$route', function($route)  {
  $route.reload();
}]);


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

app.factory( 'AllQuestionsService', function($http) {
  var questionsList = [];

  return {
    setData : function(data){
      questionsList = data;
    },
    getData : function(){
      return(questionsList)? questionsList : false;
    }
  };

});


// Needs Debugging ..
app.controller('MainCtrl', ['$scope', '$http', 'AuthService', 'CurrentQuestionService', 'AllQuestionsService', '$location', function ($scope, $http, AuthService, CurrentQuestionService, AllQuestionsService, $location) {

  $scope.$watch(AuthService.isLoggedIn, function (value, oldValue) {

    if(!value && oldValue) {
      console.log("Disconnect");
      // $location.path('/');
    }
    
    // As soon as the user logs in..
    if(value) {
      console.log("Connect");

      // Get a list of all the questions
      $http({
	method: 'GET',
	url: '/api/content/view_all_ques'
      })
	.success(function(response, status){
	  console.log(response);

	  // if (response.questions[6] === undefined) {
	  //   console.log("Hello");
	  // }
	    
	  if (response.questions.length === 0) {
	    $location.path('/question');
	  } else {
	    AllQuestionsService.setData(response.questions);
	  }

	  var temp_ques_id = response.questions[0].question_id;
	  
	  console.log("The first question is:");
	    
	  // Fetch the question details from id
	  $http({
	    method: 'GET',
	    url: '/api/content/get_question/' + temp_ques_id + "/"
	  })
	    .success(function(response, status){
	      console.log(response);
	      
	      // Set current question data 
	      CurrentQuestionService.setData(response);
		
	      // Redirect to question page
	      $location.path('/ques/' + temp_ques_id);
	    })
	    .error(function(response, status){
	      console.log("Request Failed");
	    });

	})
	.error(function(response, status){
	  console.log("Request Failed");
	});
    }

  }, true);
}]);

// For user login and logout
app.controller('LoginLogoutCtrl', ['$scope', '$http', 'AuthService', function LoginLogoutCtrl($scope, $http, AuthService){

  $scope.loginDetails = {};
  $scope.currentUserData = {};

  $scope.loginUser = function() {
    var data = {
      email: $scope.loginDetails.email,
      password: $scope.loginDetails.password
    };
    $http({
	method: 'POST',
	url: '/api/login',
	data: data
      })
	.success(function(response, status){
	  console.log("Success:", response);
	  $scope.currentUserData.userName = response.username;
	  console.log(response.username);
	  AuthService.setUser(response);
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
	  console.log("Successfully Logged out!");
	})
	.error(function(data, status){
	  console.log("Request Failed");	
	});
    console.log(AuthService.isLoggedIn());
  };

}]);

// Check why routeParams are not working
app.controller('QuestionCtrl', function QuestionCtrl($scope, $http, CurrentQuestionService) {
  $scope.questionData = {};
  $scope.askerDetails = {};
  $scope.answerData = [];
  $scope.answerCount;
  $scope.text = "";
  $scope.answerTags = [];

  // console.log("The Question id is:", $routeParams.quesId);
  var data = CurrentQuestionService.getData();
  console.log(data);
  $scope.questionData.questionId = data.question_id;
  $scope.questionData.questionText = data.question_text;
  $scope.questionData.questionTags = data.question_tags;

  
  $scope.postAnswer = function() {
    console.log($scope.text);
    console.log($scope.answerTags);
    var data = {
      question_id: $scope.questionData.questionId,
      answer: $scope.text,
      answer_tags: "abc, def"
    };
    $http({
      method: 'POST',
      url: '/api/content/add_answer',
      data: data
    })
      .success(function(response, status){
    	console.log("Success " , response);
      })
      .error(function(response, status){
    	console.log("Request Failed");
    	console.log($scope.questionData.questionId);
    });
  };

  $http({
    method: 'GET',
    url: '/api/user/' + data.user_id + '/'
  })
    .success(function(response, status){
      $scope.askerDetails.name = response.user_data[4] + " " + response.user_data[5];
    })
    .error(function(response, status){
      console.log("Request Failed");
  });

  $http({
    method: 'GET',
    url: '/api/content/get_answers/' + data.question_id + '/'
  })
    .success(function(response, status){
      console.log(response.answers[0].answer);
      $scope.answerData = response.answers;
      console.log($scope.answerData);
      $scope.answerCount = $scope.answerData.length;
      console.log($scope.answerCount);
    })
    .error(function(response, status){
      console.log("Request Failed");
    });

})

app.controller('NewUserCtrl', function NewUserCtrl($scope, $http) {
  $scope.newUserDetails = {};
  $scope.addUser = function() {
    var data = {
      email: $scope.newUserDetails.email,
      password: $scope.newUserDetails.password,
      first_name: $scope.newUserDetails.firstName,
      last_name: $scope.newUserDetails.lastName,
      method: "normal"
    };
    $http({
      method: 'POST',
      url: '/api/signup',
      data: data
    })
      .success(function(response, status){
	console.log(response);
      }).error(function(response, status){
	console.log("Request Failed");
      });
  }
});

app.controller('AddQuestionCtrl', function AddQuestionCtrl($scope, $http){
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
      })
      .error(function(response, status){
	console.log("Request Failed");
      });
  }
});

app.controller('AllQuestionsCtrl', function AllQuestionsCtrl($scope, AllQuestionsService){
  $scope.questionsList;
  $scope.questionsList = AllQuestionsService.getData();
  console.log(AllQuestionsService.getData());
});