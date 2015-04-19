// // (function(window, angular, undefined) {
//   'use strict';

//   // Module global settings.
//   var settings = {};

//   // Module global flags.
//   var flags = {
//     sdk: false,
//     ready: false
//   };

//   // Deferred Object which will be resolved when the Facebook SDK is ready
//   // and the `fbAsyncInit` function is called.
//   var loadDeferred;

//   /**
//    * @name facebook
//    * @kind function
//    * @description
//    * An Angularjs module to take approach of Facebook javascript sdk.
//    *
//    * @author Luis Carlos Osorio Jayk <luiscarlosjayk@gmail.com>
//    */
//   angular.module('facebook', []).

//     // Declare module settings value
//     value('settings', settings).

//     // Declare module flags value
//     value('flags', flags).

//     /**
//      * Facebook provider
//      */
//     provider('Facebook', [
//       function() {

//         /**
//          * Facebook appId
//          * @type {Number}
//          */
//         settings.appId = null;

//         this.setAppId = function(appId) {
//           settings.appId = appId;
//         };

//         this.getAppId = function() {
//           return settings.appId;
//         };

//         /**
//          * Locale language, english by default
//          * @type {String}
//          */
//         settings.locale = 'en_US';

//         this.setLocale = function(locale) {
//           settings.locale = locale;
//         };

//         this.getLocale = function() {
//           return settings.locale;
//         };

//         /**
//          * Set if you want to check the authentication status
//          * at the start up of the app
//          * @type {Boolean}
//          */
//         settings.status = true;

//         this.setStatus = function(status) {
//           settings.status = status;
//         };

//         this.getStatus = function() {
//           return settings.status;
//         };

//         /**
//          * Adding a Channel File improves the performance of the javascript SDK,
//          * by addressing issues with cross-domain communication in certain browsers.
//          * @type {String}
//          */
//         settings.channelUrl = null;

//         this.setChannel = function(channel) {
//           settings.channelUrl = channel;
//         };

//         this.getChannel = function() {
//           return settings.channelUrl;
//         };

//         /**
//          * Enable cookies to allow the server to access the session
//          * @type {Boolean}
//          */
//         settings.cookie = true;

//         this.setCookie = function(cookie) {
//           settings.cookie = cookie;
//         };

//         this.getCookie = function() {
//           return settings.cookie;
//         };

//         /**
//          * Parse XFBML
//          * @type {Boolean}
//          */
//         settings.xfbml = true;

//         this.setXfbml = function(enable) {
//           settings.xfbml = enable;
//         };

//         this.getXfbml = function() {
//           return settings.xfbml;
//         };

//         /**
//          * Auth Response
//          * @type {Object}
//          */

//         this.setAuthResponse = function(obj) {
//           settings.authResponse = obj || true;
//         };

//         this.getAuthResponse = function() {
//           return settings.authResponse;
//         };

//         /**
//          * Frictionless Requests
//          * @type {Boolean}
//          */
//         settings.frictionlessRequests = false;

//         this.setFrictionlessRequests = function(enable) {
//           settings.frictionlessRequests = enable;
//         };

//         this.getFrictionlessRequests = function() {
//           return settings.frictionlessRequests;
//         };

//         /**
//          * HideFlashCallback
//          * @type {Object}
//          */
//         settings.hideFlashCallback = null;

//         this.setHideFlashCallback = function(obj) {
//           settings.hideFlashCallback = obj || null;
//         };

//         this.getHideFlashCallback = function() {
//           return settings.hideFlashCallback;
//         };

//         /**
//          * Custom option setting
//          * key @type {String}
//          * value @type {*}
//          * @return {*}
//          */
//         this.setInitCustomOption = function(key, value) {
//           if (!angular.isString(key)) {
//             return false;
//           }

//           settings[key] = value;
//           return settings[key];
//         };

//         /**
//          * get init option
//          * @param  {String} key
//          * @return {*}
//          */
//         this.getInitOption = function(key) {
//           // If key is not String or If non existing key return null
//           if (!angular.isString(key) || !settings.hasOwnProperty(key)) {
//             return false;
//           }

//           return settings[key];
//         };

//         /**
//          * load SDK
//          */
//         settings.loadSDK = true;

//         this.setLoadSDK = function(a) {
//           settings.loadSDK = !!a;
//         };

//         this.getLoadSDK = function() {
//           return settings.loadSDK;
//         };

//         /**
//          * SDK version
//          */
//         settings.version = 'v2.0';

//         this.setSdkVersion = function(version) {
//           settings.version = version;
//         };

//         this.getSdkVersion = function() {
//           return settings.version;
//         };

//         /**
//          * Init Facebook API required stuff
//          * This will prepare the app earlier (on settingsuration)
//          * @arg {Object/String} initSettings
//          * @arg {Boolean} _loadSDK (optional, true by default)
//          */
//         this.init = function(initSettings, _loadSDK) {
//           // If string is passed, set it as appId
//           if (angular.isString(initSettings)) {
//             settings.appId = initSettings;
//           }

//           if(angular.isNumber(initSettings)) {
//             settings.appId = initSettings.toString();
//           }

//           // If object is passed, merge it with app settings
//           if (angular.isObject(initSettings)) {
//             angular.extend(settings, initSettings);
//           }

//           // Set if Facebook SDK should be loaded automatically or not.
//           if (angular.isDefined(_loadSDK)) {
//             settings.loadSDK = !!_loadSDK;
//           }
//         };

//         /**
//          * This defined the Facebook service
//          */
//         this.$get = [
//           '$q',
//           '$rootScope',
//           '$timeout',
//           '$window',
//           function($q, $rootScope, $timeout, $window) {
//             /**
//              * This is the NgFacebook class to be retrieved on Facebook Service request.
//              */
//             function NgFacebook() {
//               this.appId = settings.appId;
//             }

//             /**
//              * Ready state method
//              * @return {Boolean}
//              */
//             NgFacebook.prototype.isReady = function() {
//               return flags.ready;
//             };

//             NgFacebook.prototype.login = function () {

//               var d = $q.defer(),
//                   args = Array.prototype.slice.call(arguments),
//                   userFn,
//                   userFnIndex; // Converts arguments passed into an array

//                 // Get user function and it's index in the arguments array,
//                 // to replace it with custom function, allowing the usage of promises
//                 angular.forEach(args, function(arg, index) {
//                   if (angular.isFunction(arg)) {
//                     userFn = arg;
//                     userFnIndex = index;
//                   }
//                 });

//                 // Replace user function intended to be passed to the Facebook API with a custom one
//                 // for being able to use promises.
//                 if (angular.isFunction(userFn) && angular.isNumber(userFnIndex)) {
//                   args.splice(userFnIndex, 1, function(response) {
//                     $timeout(function() {

//                       if (response && angular.isUndefined(response.error)) {
//                         d.resolve(response);
//                       } else {
//                         d.reject(response);
//                       }

//                       if (angular.isFunction(userFn)) {
//                         userFn(response);
//                       }
//                     });
//                   });
//                 }

//                 // review(mrzmyr): generalize behaviour of isReady check
//                 if (this.isReady()) {
//                   $window.FB.login.apply($window.FB, args);
//                 } else {
//                   $timeout(function() {
//                     d.reject("Facebook.login() called before Facebook SDK has loaded.");
//                   });
//                 }

//                 return d.promise;
//             };

//             /**
//              * Map some asynchronous Facebook SDK methods to NgFacebook
//              */
//             angular.forEach([
//               'logout',
//               'api',
//               'ui',
//               'getLoginStatus'
//             ], function(name) {
//               NgFacebook.prototype[name] = function() {

//                 var d = $q.defer(),
//                     args = Array.prototype.slice.call(arguments), // Converts arguments passed into an array
//                     userFn,
//                     userFnIndex;

//                 // Get user function and it's index in the arguments array,
//                 // to replace it with custom function, allowing the usage of promises
//                 angular.forEach(args, function(arg, index) {
//                   if (angular.isFunction(arg)) {
//                     userFn = arg;
//                     userFnIndex = index;
//                   }
//                 });

//                 // Replace user function intended to be passed to the Facebook API with a custom one
//                 // for being able to use promises.
//                 if (angular.isFunction(userFn) && angular.isNumber(userFnIndex)) {
//                   args.splice(userFnIndex, 1, function(response) {
//                     $timeout(function() {

//                       if (response && angular.isUndefined(response.error)) {
//                         d.resolve(response);
//                       } else {
//                         d.reject(response);
//                       }

//                       if (angular.isFunction(userFn)) {
//                         userFn(response);
//                       }
//                     });
//                   });
//                 }

//                 $timeout(function() {
//                   // Call when loadDeferred be resolved, meaning Service is ready to be used.
//                   loadDeferred.promise.then(function() {
//                     $window.FB[name].apply(FB, args);
//                   });
//                 });

//                 return d.promise;
//               };
//             });

//             /**
//              * Map Facebook sdk XFBML.parse() to NgFacebook.
//              */
//             NgFacebook.prototype.parseXFBML = function() {

//               var d = $q.defer();

//               $timeout(function() {
//                 // Call when loadDeferred be resolved, meaning Service is ready to be used
//                 loadDeferred.promise.then(function() {
//                   $window.FB.XFBML.parse();
//                   d.resolve();
//                 });
//               });

//               return d.promise;
//             };

//             /**
//              * Map Facebook SDK subscribe/unsubscribe method to NgFacebook.
//              * Use it as Facebook.subscribe / Facebook.unsubscribe in the service.
//              */

//             angular.forEach([
//               'subscribe',
//               'unsubscribe',
//             ], function(name) {

//               NgFacebook.prototype[name] = function() {

//                 var d = $q.defer(),
//                     args = Array.prototype.slice.call(arguments), // Get arguments passed into an array
//                     userFn,
//                     userFnIndex;

//                 // Get user function and it's index in the arguments array,
//                 // to replace it with custom function, allowing the usage of promises
//                 angular.forEach(args, function(arg, index) {
//                   if (angular.isFunction(arg)) {
//                     userFn = arg;
//                     userFnIndex = index;
//                   }
//                 });

//                 // Replace user function intended to be passed to the Facebook API with a custom one
//                 // for being able to use promises.
//                 if (angular.isFunction(userFn) && angular.isNumber(userFnIndex)) {
//                   args.splice(userFnIndex, 1, function(response) {

//                     $timeout(function() {

//                       if (response && angular.isUndefined(response.error)) {
//                         d.resolve(response);
//                       } else {
//                         d.reject(response);
//                       }

//                       if (angular.isFunction(userFn)) {
//                         userFn(response);
//                       }
//                     });
//                   });
//                 }

//                 $timeout(function() {
//                   // Call when loadDeferred be resolved, meaning Service is ready to be used
//                   loadDeferred.promise.then(function() {
//                     $window.FB.Event[name].apply(FB, args);
//                   });
//                 });

//                 return d.promise;
//               };
//             });

//             return new NgFacebook(); // Singleton
//           }
//         ];

//       }
//     ]).

//     /**
//      * Module initialization
//      */
//     run([
//       '$rootScope',
//       '$q',
//       '$window',
//       '$timeout',
//       function($rootScope, $q, $window, $timeout) {
//         // Define global loadDeffered to notify when Service callbacks are safe to use
//         loadDeferred = $q.defer();

//         var loadSDK = settings.loadSDK;
//         delete(settings['loadSDK']); // Remove loadSDK from settings since this isn't part from Facebook API.

//         /**
//          * Define fbAsyncInit required by Facebook API
//          */
//         $window.fbAsyncInit = function() {
//           // Initialize our Facebook app
//           $timeout(function() {
//             if (!settings.appId) {
//               throw 'Missing appId setting.';
//             }

//             FB.init(settings);

//             flags.ready = true;

//             /**
//              * Subscribe to Facebook API events and broadcast through app.
//              */
//             angular.forEach({
//               'auth.login': 'login',
//               'auth.logout': 'logout',
//               'auth.prompt': 'prompt',
//               'auth.sessionChange': 'sessionChange',
//               'auth.statusChange': 'statusChange',
//               'auth.authResponseChange': 'authResponseChange',
//               'xfbml.render': 'xfbmlRender',
//               'edge.create': 'like',
//               'edge.remove': 'unlike',
//               'comment.create': 'comment',
//               'comment.remove': 'uncomment'
//             }, function(mapped, name) {
//               FB.Event.subscribe(name, function(response) {
//                 $timeout(function() {
//                   $rootScope.$broadcast('Facebook:' + mapped, response);
//                 });
//               });
//             });

//             // Broadcast Facebook:load event
//             $rootScope.$broadcast('Facebook:load');

//             loadDeferred.resolve(FB);
//           });
//         };

//         /**
//          * Inject Facebook root element in DOM
//          */
//         (function addFBRoot() {
//           var fbroot = document.getElementById('fb-root');

//           if (!fbroot) {
//             fbroot = document.createElement('div');
//             fbroot.id = 'fb-root';
//             document.body.insertBefore(fbroot, document.body.childNodes[0]);
//           }

//           return fbroot;
//         })();

//         /**
//          * SDK script injecting
//          */
//          if(loadSDK) {
//           (function injectScript() {
//             var src           = '//connect.facebook.net/' + settings.locale + '/sdk.js',
//                 script        = document.createElement('script');
//                 script.id     = 'facebook-jssdk';
//                 script.async  = true;

//             // Prefix protocol
//             // for sure we don't want to ignore things, but this tests exists,
//             // but it isn't recognized by istanbul, so we give it a 'ignore if'
//             /* istanbul ignore if */
//             if ($window.location.protocol.indexOf('file:') !== -1) {
//               src = 'https:' + src;
//             }

//             script.src = src;
//             script.onload = function() {
//               flags.sdk = true;
//             };

//             // Fix for IE < 9, and yet supported by latest browsers
//             document.getElementsByTagName('head')[0].appendChild(script);
//           })();
//         }
//       }
//     ]);

// }



// facebook module 
// angular.module('app', [''])
  // .controller('authenticationCtrl', function($scope, Facebook) {

  //   $scope.login = function() {
  //     // From now on you can use the Facebook service just as Facebook api says
  //     console.log('logged in');
  //     Facebook.login(function(response) {
  // 	console.log(response);
  //       // Do something with response.
  //     });
  //   };

  //   $scope.getLoginStatus = function() {
  //     Facebook.getLoginStatus(function(response) {
  //       if(response.status === 'connected') {
  //         $scope.loggedIn = true;
  //       } else {
  //         $scope.loggedIn = false;
  //       }
  //     });
  //   };

  //   $scope.me = function() {
  //     Facebook.api('/me', function(response) {
  //       $scope.user = response;
  //     });
  //   };
  // });


// Necessary for POST Requests to work!
var app = angular.module('travel-graph', ['ngCookies'], function($httpProvider) {
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


app.run(['$rootScope', '$location', '$cookieStore', 'AuthService', function ($rootScope, $location, $cookieStore, AuthService) {
    $rootScope.$on('$routeChangeStart', function (event) {
      
      if ($cookieStore.get('user_auth')) {
	console.log('ALLOW');
	console.log($cookieStore.get('user_auth'));
      } else {
        console.log('DENY');
	// event.preventDefault();
        // $location.path('/login');
      }
    });
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
	// templateUrl: '/static/partials/login.html',
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
app.controller('MainCtrl', ['$scope', '$http', 'AuthService', 'CurrentQuestionService', 'AllQuestionsService', '$location', '$cookieStore', function ($scope, $http, AuthService, CurrentQuestionService, AllQuestionsService, $location, $cookieStore) {

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


      $location.path('/all_questions');

      // Get a list of all the questions
      // $http({
      // 	method: 'GET',
      // 	url: '/api/content/view_all_ques'
      // })
      // 	.success(function(response, status){
      // 	  console.log(response);

      // 	  // if (response.questions[6] === undefined) {
      // 	  //   console.log("Hello");
      // 	  // }
	    
      // 	  if (response.questions.length === 0) {
      // 	    $location.path('/question');
      // 	  } else {
      // 	    // AllQuestionsService.setData(response);
      // 	    // console.log(AllQuestionsService.getData());
      // 	    $location.path('/all_questions');	    
      // 	  }

      // 	  var temp_ques_id = response.questions[0].question_id;
	  
      // 	  console.log("The first question is:");
	    
      // 	  // Fetch the question details from id
      // 	  $http({
      // 	    method: 'GET',
      // 	    url: '/api/content/get_question/' + temp_ques_id + "/"
      // 	  })
      // 	    .success(function(response, status){
      // 	      console.log(response);
	      
      // 	      // Set current question data 
      // 	      CurrentQuestionService.setData(response);
		
      // 	      // Redirect to question page
      // 	      $location.path('/ques/' + temp_ques_id);
      // 	    })
      // 	    .error(function(response, status){
      // 	      console.log("Request Failed");
      // 	    });

      // 	})
      // 	.error(function(response, status){
      // 	  console.log("Request Failed");
      // 	});
    }

  }, true);
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
	  // console.log($scope.currentUserData);
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
  
  $scope.fbLogin = function(){
    // Facebook.login(function(response){
      // console.log("Logged in with fb");
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

  };

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