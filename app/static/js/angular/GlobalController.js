var app = angular.module("GlobalApp", [
  "ngMaterial",
  "ngRoute",
  "ngAnimate",
  "ngMessages"
]);

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

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
});
