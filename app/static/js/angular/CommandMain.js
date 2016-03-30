var app = angular.module('CommandApp',[]);

app.controller('CommandControl', ['$scope', function ($scope) {
  $scope.random = "Random things and stuffs";

  $scope.CommandList = [
    {
      name: "test",
      response: "Test confirmed. :cactus",
      calls: 1,
      perm: "Mod"
    }
  ]
}]);
