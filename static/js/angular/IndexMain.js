var app = angular.module('IndexApp',[]);
var showUserHover = false;

app.controller('IndexController', ['$scope', function ($scope) {
  $scope.username = "Innectic";

  $scope.userHover = function () {
    showUserHover = !showUserHover;
    $scope.showUserHover = showUserHover;

    return $scope.showUserHover;
  }
}]);
