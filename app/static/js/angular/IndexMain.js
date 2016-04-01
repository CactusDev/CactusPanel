var app = angular.module('IndexApp', ['ngMaterial']);
var isPartnered = true;
var updateMessages = false;
var hideMessages = false;

app.controller('IndexControl', ['$scope', function ($scope) {
  $scope.isPartnered = isPartnered;

  // Temp setting of these

  // Spam prot

  $scope.messageLength = Math.floor(Math.random() * 100);
  $scope.maxCaps = Math.floor(Math.random() * 100);
  $scope.maxEmotes = Math.floor(Math.random() * 100);

  // Messages

  $scope.followText = "Thanks for the follow %user%! You rock!";
  $scope.subText = "Thanks for the sub %user%! You rock!";
  $scope.resubText = "Thanks for the resub %user% for %months% in a row! You rock!";

  // Protection things

  $scope.isProtEnabled = true;

  $scope.pressedUpdateMessages = function() {
    updateMessages = !updateMessages;
    hideMessages = !hideMessages;

    $scope.updateMessages = updateMessages;
    $scope.shouldHideChangeText = hideMessages;

    // This is where the call to the bot would go

    updateMessages = !updateMessages;
    hideMessages = !hideMessages;

    $scope.updateMessages = updateMessages;
    $scope.shouldHideChangeText = hideMessages;

    // TODO: Send a request to the bot to update all the things
  }
}]);
