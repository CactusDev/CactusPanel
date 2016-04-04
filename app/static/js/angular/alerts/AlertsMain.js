var app = angular.module('AlertsApp', ['ngMaterial', 'ngAnimate']);
var expl = false;

app.controller('AlertsControl', ['$scope', function ($scope) {

$scope.presetList = [
  "One",
  "Two",
  "Three"
]

}]);
