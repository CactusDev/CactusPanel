import { Component, OnInit } from "@angular/core";

@Component({
    selector: "sidenav",
    templateUrl: "./sidebar.component.html"
})

export class SidebarComponent implements OnInit {
    routes: Object[];

    constructor() { }

    ngOnInit() {
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
            }, {
                "route": "support",
                "name": "Support"
            }
        ];
    }
}
