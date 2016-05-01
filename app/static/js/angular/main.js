var index = angular.module('IndexApp', ['ngMaterial']);
var admin = angular.module('AdminApp', ['ngMaterial']);

index.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

admin.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

var socket = io.connect('http://' + document.domain + ':' + location.port);

index.controller('IndexControl', ['$scope', function($scope) {

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
