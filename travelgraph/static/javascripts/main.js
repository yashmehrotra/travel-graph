var app = angular.module('travel-graph', []);

app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

function AnswersCtrl($scope, $http) {
  $http.get("/api/content/get_answers/1/")
    .success(function(data, status) {
      console.log(data);
      $scope.answers = data.answers;
    }).error(function(data, status) {
      console.log("Request Failed");
    });
}