var shouldShow = true;

app.controller("TicketController", function ($scope, $mdDialog, $timeout) {

    $scope.tickets = [{
        "title": "Bot not connecting",
        "rep": "Innectic",
        "last": "Hey, my bot is broke. What happened was when I had tried to add a command, it went BOOM"
    },{
        "title": "pls gibe",
        "rep": "2Cubed",
        "last": "Me want bot. Gibe me pls."
    },{
        "title": "Backend go boom",
        "rep": "Paradigm",
        "last": "Site backend went boom. Gibe me fix nao. I want"
    },{
        "title": "My cake lied to me",
        "rep": "Glados",
        "last": "Glados, my cake lied to me. I want a new one"
    }];

    $scope.showCreate = function (ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        if (shouldShow) {
            $mdDialog.show({
                controller: null,
                templateUrl: '/ticket/new',
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

    $scope.showRespond = function (ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        if (shouldShow) {
            $mdDialog.show({
                controller: null,
                templateUrl: '/ticket/respond',
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
