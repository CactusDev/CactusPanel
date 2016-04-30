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

app.directive('padded', function () {
  return {
    restrict: 'A',
    template: "style='padding-bottom: 25px;'"
  };
});
