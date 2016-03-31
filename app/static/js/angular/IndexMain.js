var app = angular.module('IndexApp', ['ngMaterial']);
var showUserHover = false;

app.controller('IndexControl', ['$scope', function ($scope) {
  $scope.username = "Innectic";
}]);
