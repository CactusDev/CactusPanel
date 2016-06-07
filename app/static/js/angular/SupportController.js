app.controller("SupportController", ["$scope", "$mdDialog", "$mdMedia", function ($scope, $mdDialog, $mdMedia) {
    $scope.data = {};
    $scope.data.tickets = app.supportList;
    $scope.searchString = null;

    $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');

    $scope.awaitJSON = [];
    $scope.requestID = 1;

    $scope.searchSupport = function(e) {
        if (e.keyCode == 13) {
            if ($scope.searchString) {
                var packet = createJSONPacket(
                    'retrieve:search',
                    {string: $scope.searchString},
                    $scope.requestID
                );
                $scope.requestID++;

                $scope.awaitJSON.push(packet['id']);

                var request = makeRequest(
                    packet,                 // data
                    'POST',                 // method
                    '/support'              // url
                );
            } else {
                var packet = createJSONPacket(
                    'retrieve:newest',
                    {},
                    $scope.requestID
                );
                $scope.requestID++;
                $scope.awaitJSON.push(packet['id']);

                var request = makeRequest(
                    packet,                 // data
                    'POST',                 // method
                    '/support'              // url
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

                    $scope.data.tickets = data["result"]["results"];

                });
            });
        }
    }

    $scope.showCreate = function(ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

        $mdDialog.show({
            controller: CreateController,
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
            controller: ResponseController,
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

}]);

function CreateController($scope, $mdDialog) {
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
          if ($scope.issue == undefined || $scope.issue == "" ||
              $scope.details == undefined || $scope.details == "") {
              console.log('BIG BAD EXPLOSIONS!')
          }
          $scope.gotSupported = true;

          var req = makeRequest(
              createJSONPacket(
                  'create',
                  {
                      issue:      $scope.issue,
                      details:    $scope.details,
                  }
              ),
              "POST",
              "/support"
          );
          req.done(function(request) {
              request = JSON.stringify(request);
              console.log('PopupControl:166');
              console.log(request);
          });
      }
  }
}

function ReponseController($scope, $mdDialog) {
  $scope.hide = function() {
    $mdDialog.hide();
  }

  $scope.cancel = function() {
    $mdDialog.cancel();
  }

  $scope.submit = function() {

  }
}
