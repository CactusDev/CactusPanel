import { Component } from "@angular/core";

@Component({
    selector: "app-root",
    templateUrl: "./home.component.html",
    styleUrls: ["home.component.less"]
})
export class HomeComponent {
    actions: Object[];

    constructor() {
        this.actions = [
            {
                "name": "Add a user as moderator",
                "icon": "verified_user",
                "subtext": "Make someone a chat moderator.",
                "route": ""
            },
            {
                "name": "Ban a user",
                "icon": "gavel",
                "subtext": "Ban a user from chat.",
                "route": ""
            },
            {
                "name": "Timeout a user",
                "icon": "gavel",
                "subtext": "Prevent a user from chatting for an amount of time",
                "route": ""
            }
        ];
    }
}
