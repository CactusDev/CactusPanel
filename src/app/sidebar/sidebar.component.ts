import { Component } from "@angular/core";

@Component({
    selector: "sidenav",
    template: `
        <md-toolbar color="primary">
            <button md-button (click)="sidenav.toggle()">Toggle Nav</button>
        </md-toolbar>

        <md-sidenav #sidenav mode="side" class="app-sidenav">
            <h1 class="size-1">Navigation</h1>
            <nav style="margin-left:auto; margin-right:auto">
                <button *ngFor="let route of routes"
                md-raised-button color="primary"
                style="width: 95%; margin-bottom: 3%"
                [routerLink]="['/' + route.route]">{{ route.name }}</button>
            </nav>
        </md-sidenav>
    `
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
            }
        ];
    }
}
