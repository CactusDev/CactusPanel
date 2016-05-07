var index = angular.module('IndexApp', ['ngMaterial', 'ngMessages', 'material.svgAssetsCache']);
var admin = angular.module('AdminApp', ['ngMaterial']);

var socket = io.connect('http://' + document.domain + ':' + location.port);
var shouldShow = true;

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

index.config(function($interpolateProvider, $mdThemingProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');

  $mdThemingProvider.theme('default')
    .primaryPalette('green', {
      'default': "200"
    })
    .accentPalette('light-blue', {
      'default': "500"
    });
});

index.controller('IndexControl', ['$scope', '$mdDialog', '$mdMedia', function($scope, $mdDialog, $mdMedia, $timeout) {
  $scope.status = '  ';
  $scope.didClose = false;
  $scope.hasEntered = false;
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');

  $scope.showCreate = function(ev) {
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

    $mdDialog.show({
        controller: DialogController,
        templateUrl: '/support/create',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
        fullscreen: useFullScreen
      })
      .then(function(answer) {
        $scope.status = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.status = 'You cancelled the dialog.';
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
      })
      .then(function(answer) {
        $scope.status = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.status = 'You cancelled the dialog.';
      });

    $scope.$watch(function() {
      return $mdMedia('xs') || $mdMedia('sm');
    }, function(wantsFullScreen) {
      $scope.customFullscreen = (wantsFullScreen === true);
    });

  };

  $scope.showConfirmed = function(ev) {
    if (shouldShow) {

      var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;

      $mdDialog.show({
          controller: ConfirmedController,
          templateUrl: '/support/confirmed',
          parent: angular.element(document.body),
          targetEvent: ev,
          clickOutsideToClose: true,
          fullscreen: useFullScreen
        })
        .then(function(answer) {
          $scope.status = 'You said the information was "' + answer + '".';
        }, function() {
          $scope.status = 'You cancelled the dialog.';
        });

      $scope.$watch(function() {
        return $mdMedia('xs') || $mdMedia('sm');
      }, function(wantsFullScreen) {
        $scope.customFullscreen = (wantsFullScreen === true);
      });

      shouldShow = false;
    }
  };

  $scope.stuff = [{
    user: 'Innectic',
    latest: 'LOLOLOL JAVA LOLOLOL'
  }, {
    user: 'ParadigmShift3d',
    latest: 'Brunch?'
  }, {
    user: '2Cubed',
    latest: 'Wanna go get some \'taters?'
  }];

  $scope.commands = [{
    name: "!hug",
    response: "%name% hugs %args%!"
  }, {
    name: "!nerdfive",
    response: "%name% nerdfives %args%!"
  }];

  socket.on('connect', function() {
    $scope.connected = true;
    $scope.$apply();
  });

  socket.on('disconnect', function() {
    $scope.connected = false;
    $scope.$apply();
  });
}]);

function DialogController($scope, $mdDialog) {
  $scope.hide = function() {
    $mdDialog.hide();
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };

  $scope.submit = function(e) {
      if (e.which === 13) {
          if (e.button != true) {
              e.preventDefault();
          }
          if ($scope.issue == undefined || $scope.issue == '' ||
              $scope.details == undefined || $scope.details == '') {
              // @Innectic needs to add stuff to display an error under the input
          }
          $.ajax({
             url: '/support/create',
             type: 'POST',
             data: JSON.stringify({
                 issue:        $scope.issue,
                 details:      $scope.details,
             }),
             contentType: 'application/json'
          })
          .done( function(request) {
              request = JSON.stringify(request);
              console.log(request);
              if (request.success) {
                  console.log("SUCCESS!")
                  $mdDialog.hide();
                  showConfirmed($event);
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

  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
}
