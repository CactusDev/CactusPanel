var shouldShow = true;

app.controller("CreateController", function ($scope, $mdMedia, $mdDialog) {
    $scope.showCreate = function (ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        if (shouldShow) {
            $mdDialog.show({
                controller: RegisterController,
                templateUrl: '/create/popup',
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

app.controller("RegisterController", function ($scope, $mdDialog, $timeout) {
    $scope.initial = true;
    $scope.customAccount = false;
    $scope.joining = false;
    $scope.thanks = false;
    $scope.state = "Create a Bot"

    $scope.states = [
        "CactusBot",
        "CactusBotAlpha"
    ]

    $scope.login = function (from) {
        $scope.initial = false;
        $scope.joining = true;
        $scope.state = "Joining your Channel"

        if (from == "cactus") {

        } else if (from == "select") {
            $scope.choose = false;
        }

        $timeout(function () {
            $scope.thanks = true;
            $scope.joining = false;
            $scope.state = "Thank you!"
        }, 2000);
    };

    $scope.no = function () {
        $scope.choose = true
        $scope.initial = false
    }

    $scope.exit = function () {
        $mdDialog.cancel();
        document.location = 'index';
    };

    $scope.submit = function () {
        $.ajax({
                url: '/create/bot',
                type: 'POST',
                data: JSON.stringify({
                    username: $scope.username,
                    password: $scope.password,
                }),
                contentType: 'application/json'
            })
            .done(function (request) {
                console.log(JSON.stringify(request));
            });

        $mdDialog.cancel();
    };
});

function RegisterController($scope, $mdDialog, $timeout) {}
