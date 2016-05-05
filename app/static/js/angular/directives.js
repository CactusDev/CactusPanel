index.directive('pad', function() {
  return {
    restrict: 'E',
    scope: {
      loc: '@',
      amt: '@'
    },
    template: "<div style='padding-{[ loc ]}: {[ amt ]}px;'></div>"
  };
});

index.directive("createSupportTicket", function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: "{{ url_for('static', filename='js/angular/directives/CreateSupportTicket.html' }}"
  };
});

index.directive("cEmoji", function() {
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

admin.directive('pad', function() {
  return {
    restrict: 'E',
    scope: {
      loc: '@',
      amt: '@'
    },
    template: "<div style='padding-{[ loc ]}: {[ amt ]}px;'></div>"
  };
});
