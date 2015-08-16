angular.module('travelGraph')

    .config(['$routeProvider', '$locationProvider',
             function($routeProvider, $locationProvider)
             {
                 $routeProvider
                     .when('/', {
	                       templateUrl: '/dist/html/login.html',
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
	                       templateUrl: '/dist/html/login.html',
                         controller: "LoginCtrl"
                     })
                     .when('/signup', {
	                       templateUrl: '/dist/html/login.html',
                         controller: "LoginCtrl"
                     })
                     .when('/ques/:quesId', {
	                       templateUrl: '/dist/html/QnA.html',
	                       controller: 'ViewQuestionCtrl'
                     })
                     .when('/question', {
	                       templateUrl: '/dist/html/question.html',
	                       controller: 'AddQuestionCtrl'
                     })
                     .when('/all_questions', {
	                       templateUrl: '/dist/html/all_questions.html',
	                       controller: 'AllQuestionsCtrl'
                     })
                     .when('/all_tags', {
	                       templateUrl: '/dist/html/all_tags.html',
	                       controller: 'AllTagsCtrl'
                     })
                     .when('/tag/:tagName', {
	                       templateUrl: '/dist/html/tag_questions.html',
	                       controller: 'ViewTagCtrl'
                     })
                     .otherwise({
	                       redirectTo: '/'
                     });
                 $locationProvider.html5Mode(true);
             }]);
