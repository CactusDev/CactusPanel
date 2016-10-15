import { Component } from "@angular/core";

@Component({
    selector: "sidenav",
    templateUrl: "./sidebar.component.html"
})

export class SidebarComponent {
    routes: Object[];

    constructor() {
        this.routes = [
            {
                "route": "dashboard",
                "name": "Dashboard"
            }, {
                "route": "quote",
                "name": "Quotes"
            }, {
                "route": "command",
                "name": "Commands"
            }, {
                "route": "alert",
                "name": "Chat Alerts"
            }
        ];
    }
}
