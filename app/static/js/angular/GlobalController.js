var app = angular.module("GlobalApp", ["ngMaterial", "ui.router", "ui.bootstrap"]);
//

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

app.config(function($interpolateProvider, $mdThemingProvider, $stateProvider, $urlRouterProvider) {
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

  $urlRouterProvider.otherwise("/dashboard");

  $stateProvider
    .state("dashboard", { abtract: true, url:"/dash", templateUrl: {{ render_template('partials/tabs/Dashboard.html') }} })
    .state("dashboard.commands", { url: "/dash/commands", templateUrl: "{{ render_template('partials/tabs/Commands.html') }}" })
    .state("dashboard.support", { url: "/dash/support", templateUrl: "{{ render_template('partials/tabs/Support.html') }}" })

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

app.controller("TabController", function($rootScope, $scope, $state) {

  $scope.go = function(route) {
    $state.go(route)
  };

  $scope.active = function(route) {
    return $state.is(route)
  };

  $scope.tabs = [
    { heading: "Commands", route: "dashboard.commands", active: false },
    { heading: "Support", route: "dashboard.support", active: false },
  ];

  $scope.$on("$stateChangeSuccess", function() {
    $scope.tabs.forEach(function(tab) {
      tab.active = $scope.active(tab.route)
    });
  });

  // TODO: Move from here to it's own file for what it belongs to

  $scope.data = {};
  $scope.data.tickets = app.supportList;

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
})
