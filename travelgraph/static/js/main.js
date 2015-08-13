angular.module('travelGraph', ['ngRoute', 'ngStorage', 'ngFacebook',
                               'travelGraph.user', 'travelGraph.qna',
                               'travelGraph.tags', 'travelGraph.question'])

    .config(function($facebookProvider) {
        $facebookProvider.setAppId('1423273901281785');
    })

    // Whenever a new route has to be added, add it here as well as in views.py
    .config(['$routeProvider', '$locationProvider',
             function($routeProvider, $locationProvider)
             {
                 $routeProvider
                     .when('/', {
	                       templateUrl: '/static/build/html/login.html',
                         controller: "LoginCtrl",
                         // resolve : {
                         //     requestToken : function($http, $q) {
                         //         var reqUrl = "/api/user/request_key";
                         //         var deferred = $q.defer();
                         //         $http.get(reqUrl)
                         //             .then(
                         //                 function(res) {
                         //                     console.log(res);
                         //                     deferred.resolve(res);
                         //                 },
                         //                 function() {
                         //                     deferred.reject();
                         //                     // Request fails
                         //                 }
                         //                 return deferred.promise;
                         //             );
                         //     }
                         // }
                     })
                     .when('/login', {
	                       templateUrl: '/static/build/html/login.html',
                         controller: "LoginCtrl"
                     })
                     .when('/signup', {
	                       templateUrl: '/static/build/html/login.html',
                         controller: "LoginCtrl"
                     })
                     .when('/ques/:quesId', {
	                       templateUrl: '/static/build/html/QnA.html',
	                       controller: 'ViewQuestionCtrl'
                     })
                     .when('/question', {
	                       templateUrl: '/static/build/html/question.html',
	                       controller: 'AddQuestionCtrl'
                     })
                     .when('/all_questions', {
	                       templateUrl: '/static/build/html/all_questions.html',
	                       controller: 'AllQuestionsCtrl'
                     })
                     .when('/all_tags', {
	                       templateUrl: '/static/build/html/all_tags.html',
	                       controller: 'AllTagsCtrl'
                     })
                     .when('/tag/:tagName', {
	                       templateUrl: '/static/build/html/tag_questions.html',
	                       controller: 'ViewTagCtrl'
                     })
                     .otherwise({
	                       redirectTo: '/'
                     });
                 $locationProvider.html5Mode(true);
             }])

    .run(function($rootScope, $location, $timeout) {
        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

        $rootScope.$on("$routeChangeStart",
                       function(event, nextRoute)
                       {
                           var LOGIN_TMPL = "/static/build/html/login.html";
                           $timeout(function() {
                               if ($rootScope.loggedUser == null) {
                                   if (typeof nextRoute.loadedTemplateUrl ===
                                       'undefined' ||
                                       nextRoute.loadedTemplateUrl ===
                                       LOGIN_TMPL)
                                   {
                                       console.log("No redirect for this route");
                                   } else {
                                       $location.path("/");
                                       console.log("Not logged in.. redirected");
                                   }
                               }
                           });
                       }
                      );
    })

    // App-wide controller
    .controller('MainCtrl',
                ['$scope', '$location',
                 function ($scope, $location)
                 { }])

    // To handle Login and Signup
    .controller('LoginCtrl',
                ['$scope', '$http', '$facebook',
                 function ($scope, $http, $facebook)
                 {
                     $scope.requestInvite = false;
                     $scope.loginMsg = "";
                     $scope.fbLoginLoader = false;
                     $scope.successLogin = false;

                     $scope.fbLogin = function(ev) {
                         $scope.fbLoginLoader = true;
                         $scope.successLogin = false;
                         $facebook.login().then(
                             function(res) {
                                 console.log(res);
                                 $scope.fbLoginLoader = false;
                                 if (typeof res.status !== 'undefined') {
                                     $scope.successLogin = true;
                                     $scope.loginMsg = 'Login Successful.';
                                     $facebook.api('/me').then(
                                         function(res) {
                                             console.log(res);
                                             $scope.loginMsg = 'Redirecting....';
                                         },
                                         function() {
                                             $scope.successLogin = false;
                                             console.log('Error');
                                             // Error
                                         }
                                     );
                                 }
                                 else {
                                     $scope.successLogin = false;
                                     $scope.loginMsg = 'Some error occured. Please try again later';
                                 }
                             },
                             function() {
                                 $scope.fbLoginLoader = false;
                                 $scope.successLogin = false;
                                 $scope.loginMsg = 'Some error occured. Please try again later';
                             }
                         );
                     };

                     $scope.gPlusLogin = function(ev) {
                         // Login through Google+
                     };

                     $scope.invite = function(ev) {
                         // Invite(POST request with 'email' parameter)
                     }
                 }])

    .directive('closeMsg', function() {
        return {
            restrict: 'E',
            template: '<i class="close icon" ng-click="remove()"></i>',
            replace: true,
            link: function(scope, elm, attrs) {
                scope.remove = function() {
                    var el = elm.parent();
                    $(el).fadeOut();
                };
            }
        }
    })

    .directive('ckEditor', function() {
        return {
            require: '?ngModel',
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
    });
