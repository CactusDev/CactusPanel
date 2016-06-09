var app = angular.module("GlobalApp", [])
// , $routeProvider, $mdThemingProvider
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');

  // $mdThemingProvider.theme('default')
  //     .primaryPalette('green', {
  //         'default': "900",
  //         'hue-1': "600"
  //     })
  //     .accentPalette('light-blue', {
  //         'default': "A200"
  // });
});
//   $routeProvider.when("/", {
//     templateUrl: "/tab/dash"
//   }).when("/dashboard/commands", {
//     templateUrl: "/tab/commands"
//   }).when("/dashboard/support", {
//     templateUrl: "/tab/support",
//     controller: "SupportController"
//   }).otherwise({ redirectTo: "/" });
// });

app.controller("GlobalController", function($scope) {
  $scope.stuff = "tato2";
});
