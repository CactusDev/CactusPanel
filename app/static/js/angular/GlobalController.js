var app = angular.module("GlobalApp", ["ngMaterial", "ngRoute"])

app.config(function($interpolateProvider, $mdThemingProvider, $routeProvider, $locationProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');

  $mdThemingProvider.theme('default')
      .primaryPalette('green', {
          'default': "900",
          'hue-1': "600"
      })
      .accentPalette('light-blue', {
          'default': "A200"
  });
  
  $locationProvider.hashPrefix('');

  $routeProvider.when("/", {
    templateUrl: "partial/dash"
  }).when("/commands", {
    templateUrl: "partial/commands"
  }).when("/quotes", {
    templateUrl: "partials/quotes"
  }).otherwise({ redirectTo: "/" });
});

app.controller("GlobalController", function($scope, $location) {
  var gl = this;

  gl.changeView = function(route) {
    $location.path(route)
  }
});
