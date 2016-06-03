$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken)
        }
    }
});

app.controller('PopupControl', ['$scope', '$mdDialog', '$mdMedia', function($scope, $mdDialog, $mdMedia, $timeout) {
    $scope.status = '  ';
    $scope.didClose = false;
    $scope.hasEntered = false;
    $scope.gotSupported = false;
    $scope.addedCommand = false;
    $scope.addingCommand = false;
    $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');
    $scope.searchString = null;

    $scope.awaitJSON = [];

    $scope.searchSupport = function(e) {
        if (e.keyCode == 13) {
            if ($scope.searchString) {
                var packet = createJSONPacket(
                    'tickets:retrieve:search',
                    {string: $scope.searchString},
                );

                $scope.awaitJSON.push(packet['id']);

                var request = retrieveTickets(
                    packet,
                    'POST',
                )
            } else {
                var packet = createJSONPacket(
                    'tickets:retrieve:newest',
                    {},
                )
                $scope.awaitJSON.push(packet['id']);

                var request = retrieveTickets(
                    packet,
                    'GET',
                );
            }

            request.done(function(data) {
                console.log('PopupControl:49');
                console.log(data);
                var indexID = $scope.awaitJSON.indexOf(data['id']);
                if (indexID > -1) {
                    $scope.awaitJSON.splice(indexID, 1);
                } else {
                    console.warn('NOTE: Unexepected ID', data['id'], 'returned by server!')
                }

                $scope.$apply(function() {
                    $scope.data.tickets.length = 0;

                    $scope.data.tickets = data;

                });
                //   var diff = _.differenceBy(data, $scope.tickets, (item, key, a) => item.id);
                //   $scope.$apply(function() {
                //       for (ticket in diff) {
                //           $scope.tickets.push(diff[ticket]);
                //       }
                //   });
            });
        }
    }

    $scope.showCreate = function(ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        $mdDialog.show({
            controller: DialogController,
            templateUrl: '/support/create',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: useFullScreen
        });

        $scope.$watch(function() {
            return $mdMedia('xs') || $mdMedia('sm');
        }, function(wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
        });

    };

    $scope.showRespond = function(ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        $mdDialog.show({
            controller: DialogController,
            templateUrl: '/support/respond',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: useFullScreen
        });

        $scope.$watch(function() {
            return $mdMedia('xs') || $mdMedia('sm');
        }, function(wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
        });

    };

    $scope.showAddCommand = function(ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        $mdDialog.show({
            controller: CommandController,
            templateUrl: '/command/create',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: useFullScreen
        });

        $scope.$watch(function() {
            return $mdMedia('xs') || $mdMedia('sm');
        }, function(wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
        });

    }
}]);

function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
        $mdDialog.hide();
    };

    $scope.cancel = function() {
        $mdDialog.cancel();
    };

    $scope.submit = function(e) {
        if (e.which === 13) {
            if (e.button != true) {
                e.preventDefault();
            }
            if ($scope.issue == undefined || $scope.issue == '' ||
                $scope.details == undefined || $scope.details == '') {
                console.log('BIG BAD EXPLOSIONS!')
            }
            $scope.gotSupported = true;

            var req = makeRequest(
                createJSONPacket(           // JSON-RPC packet
                    'tickets:create',           // method
                    {                           // data
                        issue:      $scope.issue,
                        details:    $scope.details,
                    },
                ),
                'POST',                     // method
                '/support'                  // url
            );
            req.done(function(request) {
                request = JSON.stringify(request);
                console.log('PopupControl:166');
                console.log(request);
            });
        }
    }
}

function ConfirmedController($scope, $mdDialog) {
    $scope.cancel = function() {
        $scope.didClose = true;

        $mdDialog.cancel();
    };
}

function CommandController($scope, $mdDialog, $timeout) {
    $scope.showCreate = true;
    $scope.cancel = function() {
        $mdDialog.cancel();
    };

    $scope.addCommand = function() {
        $scope.showCreate = false;

        $timeout(function() {
            $scope.addedCommand = true;
            $scope.addingCommand = false;
        }, 2000);

        $scope.addingCommand = true;
    }
}
