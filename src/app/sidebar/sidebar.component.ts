import { Component, OnInit } from "@angular/core";
import { Location } from "@angular/common";
import { RouterModule } from "@angular/router";

@Component({
    selector: "sidenav",
    templateUrl: "./sidebar.component.html"
})

export class SidebarComponent implements OnInit {
    routes: Object[];

    moveToCode() {
        this.location.go("/code");
    }

    constructor(private location: Location) { }

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
            }
        ];
    }
}
