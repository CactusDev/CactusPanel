var app = angular.module("GlobalApp", [
  "ngMaterial",
  "ngRoute"
]);

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

  var req = makeRequest(
      createJSONPacket(               // data
         'retrieve:newest',               // method
         {},                              // params
         0                                // id
      ),
      'POST',                         // type
      '/support'                      // url
  );
  req.done(function(request) {
      if (request.hasOwnProperty("error")) {
          // It looks like we've got an error, deal with it
      } else if (request.hasOwnProperty("result")) {
          // Success!
          app.supportList = request["result"]["results"];
      }
  });
});

app.controller("GlobalController", function($scope, $location) {
  var gl = this;

  gl.changeView = function(route) {
    $location.path(route)
  }
});
