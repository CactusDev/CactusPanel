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
