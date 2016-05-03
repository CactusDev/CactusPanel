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
