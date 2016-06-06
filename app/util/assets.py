from flask.ext.assets import Environment, Bundle
from .. import app

assets = Environment(app)

bundles = {

    "angular_material_js": Bundle(
        "js/libs/angular.min.js",
        "js/libs/angular-animate.min.js",
        "js/libs/angular-aria.min.js",
        "js/libs/angular-material.min.js",
        "js/libs/angular-messages.min.js",
        "js/libs/angular-route.min.js",
        "js/libs/svg-assets-cache.js",
        filters="jsmin",
        output="gen/angular-material.js"),

    "angular_material_css": Bundle(
        "css/libs/angular-material.min.css",
        filters="cssmin",
        output="gen/angular-material.css"),

    "dashboard_js": Bundle(
        "js/libs/jquery.min.js",
        "js/libs/socket.io.min.js",
        "js/libs/lodash.min.js",
        "js/angular/GlobalController.js",
        "js/angular/PopupController.js",
        "js/angular/directives.js",
        "js/socket.js",
        filters="jsmin",
        output="gen/dashboard.js")
}

assets.register(bundles)
