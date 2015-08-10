angular.module('travelGraph', ['ngRoute', 'ngStorage', 'ngFacebook',
                               'travelGraph.user', 'travelGraph.qna',
                               'travelGraph.tags', 'travelGraph.question'])

    .config(function($facebookProvider) {
        $facebookProvider.setAppId('1423273901281785');
    })

    // Whenever a new route has to be added, add it here as well as in views.py
    .config(['$routeProvider', '$locationProvider',
             function($routeProvider, $locationProvider) {
                 $routeProvider
                     .when('/', {
	                       templateUrl: '/static/build/html/home.html',
                         controller: "LoginCtrl"
                     })
                     .when('/login', {
	                       templateUrl: '/static/build/html/login.html',
                         controller: "LoginCtrl"
                     })
                     .when('/signup', {
	                       templateUrl: '/static/build/html/signup.html',
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

    .run(function($rootScope) {
        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    })

    // App-wide controller
    .controller('MainCtrl', ['$scope', function ($scope) {
        // Globally used variables here.
    }])

    // To handle Login and Signup
    .controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {
        // Login/Logout logic.
    }]);
