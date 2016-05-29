function isIn(object, array) {
    for (var i = 0, len = array.length; i < len; i++) {
        if (object.id == array[i].id) {
            return true;
            break;
        }
    }

    // Made it this far, so it's NOT in the array
    return false;
};

Array.prototype.unique = function () {
    var output = new Array;
    for (var i = 0, len = this.length; i < len; i++) {
        if (!isIn(this[i], output)) {
            output.push(this[i]);
        }
    }

    return output;
};

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
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

  $scope.searchSupport = function(e) {
      $scope.keyCode = e.keyCode;
      console.log(e.keyCode);
      if (e.keyCode == 13) {
          var request = $scope.retrieveTickets();
          request.done(function(data) {
              $scope.tickets = $scope.tickets.concat(data);
              $scope.tickets = $scope.tickets.unique();
              console.log($scope.tickets);
              // NOTE:  concatenation & de-duplication works, need to get Angular to stop being poop and make it update visible tickets
          });
      }
  }

  $scope.retrieveTickets = function(e, type, data) {
      if (data == undefined || data == '') {
          var type = 'GET';
      }
     var req = $.ajax({
          url: '/support/list',
          type: type,
          data: JSON.stringify(data),
          contentType: 'application/json'
      });

      return req;
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
        console.log("BIG BAD EXPLOSIONS!")
      }
      $scope.gotSupported = true;

      $.ajax({
          url: '/support/create',
          type: 'POST',
          data: JSON.stringify({
            issue: $scope.issue,
            details: $scope.details,
          }),
          contentType: 'application/json'
        })
        .done(function(request) {
          request = JSON.stringify(request);
          console.log(request);
          if (request.success) {
            console.log("SUCCESS!")
          }
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
