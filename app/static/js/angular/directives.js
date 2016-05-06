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
