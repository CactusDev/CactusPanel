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
    $scope.expanded = false;

    $scope.states = [
        "CactusBot",
        "CactusBotAlpha"
    ]

    $scope.checkVal = () => {
        if (window.passed) {
            // Fade the dialog to the next status
            $timeout(() => {
                $scope.thanks = true;
                $scope.joining = false;
                $scope.state = 'Thank you!';
            }, 2000);
        } else if (!window.passed) {
            // TODO: Make it show errors
            $timeout(() => {
                $scope.thanks = true;
                $scope.joining = false;
                $scope.state = 'Oh bother. Something went wrong.';
                console.log(window.errors);
            }, 2000);
        } else if (window.exists) {
            // TODO: Make this link
            $timeout(() => {
                $scope.thanks = true;
                $scope.joining = false;
                $scope.state = 'Looks like you\'re already good to go! <br /> If you want to change you bot config, do it <a href="url for config">here</a>';
            }, 2000);
        } else {
            // Wait a bit, then check again
            setTimeout(() => {
                $scope.checkVal();
            }, 10);
        }
    }

    $scope.login = function (from) {
       $scope.initial = false;
       $scope.joining = true;
       $scope.state = "Joining your Channel"

       if (from == "cactus") {

       } else if (from == "select") {
           $scope.choose = false;
           $scope.expanded = true;
       }

       window.open("/authorize/beam");

       setTimeout(() => {
           $scope.checkVal();
       }, 10);
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
