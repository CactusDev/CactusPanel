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
    //  /support returns when method is set to 'retrieve:newest'
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
        console.log('app.config(TabControllerler:39)');
        console.log(request);
        if (request.hasOwnProperty("error")) {
            // It looks like we've got an error, deal with it
        } else if (request.hasOwnProperty("result")) {
            // Success!
            app.supportList = request["result"]["results"];
        }
    })
});


app.controller('TabController', ['$scope', function($scope) {
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
