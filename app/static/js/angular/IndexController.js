var app = angular.module('IndexApp', ['ngMaterial']);

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


app.controller('IndexControl', ['$scope', function($scope) {

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
