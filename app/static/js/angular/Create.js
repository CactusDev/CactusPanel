var shouldShow = true;

app.controller("CreateController", function($scope, $mdMedia, $mdDialog) {
  $scope.showCreate = function(ev) {
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

    if (shouldShow) {
      $mdDialog.show({
        controller: RegisterController,
        templateUrl: '/create/popup',
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

      shouldShow = false;
    }
  };
});

function RegisterController($scope, $mdDialog, $timeout) {
  $scope.initial = true;
  $scope.customAccount = false;
  $scope.joining = false;
  $scope.setup = false;

  $scope.slowProceed = function(time) {
    $timeout($scope.setup = true, slide);
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.submit = function() {
    $.ajax({
        url: '/create/bot',
        type: 'POST',
        data: JSON.stringify({
          username: $scope.username,
          password: $scope.password,
        }),
        contentType: 'application/json'
      })
      .done(function(request) {
        console.log(JSON.stringify(request));
      });

      $mdDialog.cancel();
  }
}
