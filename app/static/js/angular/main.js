var index = angular.module('IndexApp', ['ngMaterial']);
var admin = angular.module('AdminApp', ['ngMaterial']);

index.config(function($interpolateProvider, $mdThemingProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');

    $mdThemingProvider.theme('default')
    .primaryPalette('green', {
      'default': "900"
    })
    .accentPalette('light-blue', {
      'default': "900"
    });
});

admin.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

var socket = io.connect('http://' + document.domain + ':' + location.port);

index.controller('IndexControl', ['$scope', function($scope) {

  $scope.stuff = [
    {
    user: 'Innectic',
    latest: 'LOLOLOL JAVA LOLOLOL'
    },
    {
      user: 'ParadigmShift3d',
      latest: 'Brunch?'
    },
    {
      user: '2Cubed',
      latest: 'Wanna go get some tttttaters?'
    }

];

    socket.on('connect', function() {
        $scope.connected = true;
        $scope.$apply();
    });

    socket.on('disconnect', function() {
        $scope.connected = false;
        $scope.$apply();
    });
}]);

admin.controller('AdminControl', ['$scope'], function($scope) {

});
