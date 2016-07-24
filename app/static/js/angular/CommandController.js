var shouldShow = true;

app.controller("CommandController", function ($scope, $mdDialog, $timeout) {

    $scope.commands = [{
        "command": "potato",
        "response": "hoi! I like tatos!",
        "enabled": true
    },{
        "command": "stuff",
        "response": "THINGS!",
        "enabled": false
    },{
        "command": "boop",
        "response": "BOOP! @%ARG1%",
        "enabled": true
    }];

    $scope.showCreate = function (ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        if (shouldShow) {
            $mdDialog.show({
                controller: null,
                templateUrl: '/command/new',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: false,
                fullscreen: useFullScreen
            });
            $scope.$watch(function () {
                return $mdMedia('xs') || $mdMedia('sm');
            }, function (wantsFullScreen) {
                $scope.customFullscreen = (wantsFullScreen === true);
            });

            shouldShow = false;
        }
    };
});
