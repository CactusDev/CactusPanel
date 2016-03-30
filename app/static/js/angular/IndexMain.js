var app = angular.module('IndexApp',[]);
var showUserHover = false;

app.controller('IndexControl', ['$scope', function ($scope) {
  $scope.username = "Innectic";

  $scope.userHover = function () {
    showUserHover = !showUserHover;
    $scope.showUserHover = showUserHover;

    return $scope.showUserHover;
  }
}]);
