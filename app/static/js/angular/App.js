
app.controller('AppCtrl', function ($scope, $mdSidenav) {
  $scope.navOpen = false;

  $scope.close = function() {
    $mdSidenav('left').close();
  }

  $scope.open = function() {
    $mdSidenav('left').open();
  }

  $scope.toggle = function() {
    if($scope.navOpen == true) {
      $mdSidenav('left').close();
    } else {
      $mdSidenav('left').open();
    }

    $scope.navOpen = !$scope.navOpen;
  }

  $scope.locations = [{
      name: "Dashboard",
      partial: "/"
    }, {
      name: "Commands",
      partial: "/commands"
    }, {
      name: "Quotes",
      partial: "/quotes"
    }, {
      name: "Goals",
      partial: "/goals"
    }];
});
