var app = angular.module("GlobalApp", [
  "ngMaterial",
  "ngRoute"
]);

var socket = io.connect('http://' + document.domain + ':' + location.port);
var shouldShow = true;

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

app.config(function($interpolateProvider, $mdThemingProvider, $routeProvider) {
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

  $routeProvider.when("/", {
    templateUrl: "/tab/dash"
  }).when("/dashboard/commands", {
    templateUrl: "/tab/commands"
  }).when("/dashboard/support", {
    templateUrl: "/tab/support",
    controller: "SupportController"
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

app.controller("TabController", function($scope, $window) {
  // TODO: Move from here to it's own file for what it belongs to


  $scope.commands = [{
      name: "!hug",
      response: "%name% hugs %args%!"
  }, {
      name: "!nerdfive",
      response: "%name% nerdfives %args%!"
  }];

  socket.on('connect', function() {
      $scope.connected = true;
      $scope.$apply();
  });

  socket.on('disconnect', function() {
      $scope.connected = false;
      $scope.$apply();
  });

  $scope.dash = function() {
    $window.location.href='#';
  }

  $scope.commands = function() {
    $window.location.href='#dashboard/commands';
  }

  $scope.support = function() {
    $window.location.href='#dashboard/support';
  }
});
