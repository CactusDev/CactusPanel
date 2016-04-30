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

index.directive('padded', function () {
  return {
    restrict: 'A',
    template: "style='padding-bottom: 25px;'"
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

admin.directive('padded', function () {
  return {
    restrict: 'A',
    template: "style='padding-bottom: 25px;'"
  };
});
