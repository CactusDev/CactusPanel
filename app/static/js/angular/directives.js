app.directive('pad', function() {
  return {
    restrict: 'E',
    scope: {
      loc: '@',
      amt: '@'
    },
    template: "<div style='padding-{[ loc ]}: {[ amt ]}px;'></div>"
  };
});

app.directive("cEmoji", function() {
  return {
    restrict: 'E',
    scope: {
      emoji: '@',
      x: '@',
      y: '@'
    },
    templateUrl: "/c-emoji"
  }
});

// --------------------------
// TABS
// --------------------------

app.directive("dash", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "/tab/dash"
  }
});

app.directive("botSettings", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "/tab/botsettings"
  }
});

app.directive("commands", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "/tab/commands"
  }
});

app.directive("support", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "/tab/support"
  }
});

app.directive("userSettings", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "/tab/usersettings"
  }
});
