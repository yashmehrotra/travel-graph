var app = angular.module('travel-graph', []);

// app.run(function($rootscope)) {
//   $rootscope.name = "Avijit Gupta";
// });

// app.controller('Logged-in-user', ['$scope', function($scope) {
  
// }]);

app.controller('answers-get'['$scope', function($scope) {
  
  var ques_id = document.getElementById('ques-id').text();

  $http({
    url: "/api/content/get_answers" + ques_id + "/",    // edit here
    method: "GET"
  }).success(function(data, status) {
    console.log("Data is: " + data);
  }).error(function(data, status){
    console.log("Request Failed");
  }); 

}]);