var index = angular.module('IndexApp', ['ngMaterial']);
var admin = angular.module('AdminApp', ['ngMaterial']);

var socket = io.connect('http://' + document.domain + ':' + location.port);

index.config(function($interpolateProvider, $mdThemingProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');

  $mdThemingProvider.theme('default')
    .primaryPalette('green', {
      'default': "200"
    })
    .accentPalette('light-blue', {
      'default': "500"
    });
});

index.controller('IndexControl', ['$scope', function($scope) {

  $scope.stuff = [{
    user: 'Innectic',
    latest: 'LOLOLOL JAVA LOLOLOL'
  }, {
    user: 'ParadigmShift3d',
    latest: 'Brunch?'
  }, {
    user: '2Cubed',
    latest: 'Wanna go get some \'taters?'
  }];

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
}]);
