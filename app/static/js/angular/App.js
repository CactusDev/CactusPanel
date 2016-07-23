
app.controller('AppCtrl', function ($scope, $mdSidenav) {
  $scope.navOpen = false;
  $scope.state = "Dashboard";

  $scope.close = function() {
    $mdSidenav('left').close();
  }

  $scope.open = function() {
    $mdSidenav('left').open();
  }

  $scope.setState = function(newState) {
    $scope.state = newState;
  }

  $scope.toggle = function() {
    if($scope.navOpen == true) {
      $mdSidenav('left').close();
    } else {
      $mdSidenav('left').open();
    }

    $scope.navOpen = !$scope.navOpen;
  }

  $scope.locations = [
    "Dashboard",
    "Commands",
    "Quotes",
    "Goals",
    ];
});
