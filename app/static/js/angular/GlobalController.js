var app = angular.module("GlobalApp", ["ngMaterial"])
// , $routeProvider
app.config(function($interpolateProvider, $mdThemingProvider) {
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
});

app.controller("GlobalController", function($scope) {
  var vm = this;
});
