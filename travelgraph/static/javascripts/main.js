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

// For ckeditor integration in AngularJS
app.directive('ckEditor', [function () {
  return {
    require: '?ngModel',
    restrict: 'C',
    link: function(scope, elm, attr, ngModel) {
      var ck = CKEDITOR.replace(elm[0]);
      
      if (!ngModel) return;
      
      ck.on('pasteState', function() {
        scope.$apply(function() {
          ngModel.$setViewValue(ck.getData());
          
        });
      });   
      
      ngModel.$render = function(value) {
        ck.setData(ngModel.$viewValue);
      };
    }
  };
}]);


// Prevent conflict with Flask!
app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// For user to login/logout + storing current user data
app.factory('UserSession', function($http) {
  var currentUser;

  return {
    login: function($http, data) { 
      console.log("Data Received:", data);
      $http({
  method: 'POST',
  url: "/api/login", 
  data: data,
      })
      .success(function(data, status) {
  console.log("Success: ", data);
  window.location.replace('/ques/1');
      })
      .error(function(data, status){
  console.log("Request Failed");      
      });
    },
    logout: function($http) {
      $http.get("/api/logout")
  .success(function(data, status) {
    console.log(data);
  }).error(function(data, status){
    console.log("Logout Request Failed");
  });
    },
    isLoggedIn: function(param) { 
      console.log(param , "Received");
      if (param) { 
  return true; 
      }
  return false;
    }, 
  }
});

// Login user from login.html view
app.controller('LoginCtrl', ['$scope', '$http', 'UserSession', function LoginCtrl($scope, $http) {
  $scope.loginDetails = {};
  var data = {
    'email': $scope.loginDetails.email,
    'password': $scope.loginDetails.password,
  };
  console.log("Data sent:" , data);
  $scope.loginUser = UserSession.login(data);
  $scope.$watch( UserSession.isLoggedIn, function() {
    $scope.isLoggedIn = UserSession.isLoggedIn(true);
  });
}]);

app.controller('GetAnswersCtrl', ['$scope', '$http', function GetAnswersCtrl($scope, $http) {
  $http.get("/api/content/get_answers/1/")
    .success(function(data, status) {
      $scope.answers = data.answers;
    }).error(function(data, status) {
      console.log("Request Failed");
    });
}]);

app.controller('PostAnswerCtrl', ['$scope', '$http', function PostAnswerCtrl($scope, $http) {
  $scope.postAnswer = function() {
    var data = {
      // 'question_id': ,              // re-think implementation again
      'answer': $scope.value,
    };
    $http({
      method: 'POST',
      url: "/api/content/add_answer", 
      data: data,
    })
      .success(function(data, status) {
  console.log(data);
  $scope.answers = data.answers;
      }).error(function(data, status) {
  console.log("Request Failed");
      });
  };
}])