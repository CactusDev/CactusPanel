import { Component, OnInit } from "@angular/core";

@Component({
    selector: "app-root",
    templateUrl: "./support.component.html",
    styleUrls: ["support.component.less"]

})
export class SupportComponent implements OnInit {
    addingTicket: boolean = false;

    constructor() { }

    ngOnInit() {
    }
}
