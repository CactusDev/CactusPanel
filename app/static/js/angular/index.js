var app = angular.module('IndexApp', ['ngMaterial']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

var isPartnered = true;
var updateMessages = false;
var hideMessages = false;
var spinner = false;

var socket = io.connect('http://' + document.domain + ':' + location.port);

app.controller('IndexControl', ['$scope', function($scope) {

    socket.on('connect', function() {
        $scope.connected = true;
        $scope.$apply();
    });

    socket.on('disconnect', function() {
        $scope.connected = false;
        $scope.$apply();
    });

    $scope.isPartnered = isPartnered;

    // Temp setting of these

    // Spam prot

    $scope.messageLength = Math.floor(Math.random() * 100);
    $scope.maxCaps = Math.floor(Math.random() * 100);
    $scope.maxEmotes = Math.floor(Math.random() * 100);

    // Messages

    $scope.followText = "Thanks for the follow %user%! You rock!";
    $scope.subText = "Thanks for the sub %user%! You rock!";
    $scope.resubText = "Thanks for the resub %user% for %months% in a row! You rock!";

    // Protection things

    $scope.isProtEnabled = true;

    $scope.pressedUpdateMessages = function() {
        updateMessages = !updateMessages;
        hideMessages = !hideMessages;
        spinner = !spinner;

        $scope.shouldDisplayLoader = spinner;

        $scope.updateMessages = updateMessages;
        $scope.shouldHideChangeText = hideMessages;

        updateMessages = !updateMessages;
        hideMessages = !hideMessages;

        $scope.updateMessages = updateMessages;
        $scope.shouldHideChangeText = hideMessages;

        packet = {
            followMessage: $scope.followText,
            subMessage: $scope.subText,
            resubMessage: $scope.resubText
        };

        socket.emit("updateAlerts", packet);

        socket.on('updateComplete', function() {
            spinner = !spinner;

            $scope.shouldDisplayLoader = spinner;

            console.log('Update for alerts complete');
        });
    }

    $scope.priorities = [{
        id: 1,
        name: "Low"
    }, {
        id: 2,
        name: "Medium"
    }, {
        id: 3,
        name: "High"
    }, {
        id: 4,
        name: "Urgent"
    }]

    $scope.commandList = [{
        id: 1,
        command: "hug",
        response: "%name% hugs %args%!",
        calls: 73,
        author: 2547 // Beam user ID
    }, {
        id: 2,
        command: "highfive",
        response: "%name% highfives %args%!",
        calls: 9,
        author: 252247 // Beam user ID
    }]
}]);
