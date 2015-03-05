// Your app's root module...
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

app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


app.factory('UserSession', function($http) {
  var currentUser;

  return {
    login: function($http) { 
      // $http.post("/api/", );
    },
    logout: function($http) {
      $http.get("/api/logout")
	.success(function(data, status) {
	  console.log(data);
	}).error(function(data, status){
	  console.log("Logout Request Failed");
	});
    },
    // isLoggedIn: function() { },  // check status (logged in/logged out)
  }
});

// Login user from login.html page
app.controller('LoginCtrl', ['$scope', '$http', function LoginCtrl($scope, $http) {
  $scope.loginDetails = {};
  $scope.loginUser = function (){
    console.log($scope.loginDetails);
    $http({
      method: 'POST',
      url: "/api/login", 
      data: {
      	'email': $scope.loginDetails.email,
      	'password': $scope.loginDetails.password,
      },
    })
    .success(function(data, status) {
      console.log("Success: ", data);
      window.location.replace('/ques/1');
    })
    .error(function(data, status){
      console.log("Request Failed");      
    });
  };
}]);


function AnswersCtrl($scope, $http) {
  $http.get("/api/content/get_answers/1/")
    .success(function(data, status) {
      console.log(data);
      $scope.answers = data.answers;
    }).error(function(data, status) {
      console.log("Request Failed");
    });
}