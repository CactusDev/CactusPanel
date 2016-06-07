app.controller('CommandsController', ['$scope', '$mdDialog', '$mdMedia', function($scope, $mdDialog, $mdMedia, $timeout) {

  $scope.addedCommand = false;
  $scope.addingCommand = false;
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');

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
