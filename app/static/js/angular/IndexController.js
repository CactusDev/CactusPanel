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
    // Initial population of list, so just go by date submitted, which GET-ing
    //  /support returns when method is set to 'tickets:retrieve:newest'
    var req = makeRequest(
        createJSONPacket(               // data
           'tickets:retrieve:newest',       // method
           {},                              // params
        ),
        'GET',                          // type
        '/support'                      // url
    );
    req.done(function(request) {
        console.log('app.config(indexController:39)');
        console.log(request);
        app.supportList = request;
    })
});


app.controller('IndexControl', ['$scope', function($scope) {
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
}]);
