import { Component, OnInit } from "@angular/core";

@Component({
    selector: "app-root",
    templateUrl: "./code.component.html",
    styleUrls: ["code.component.less"]

})
export class CodeComponent implements OnInit {
    state: string = "";

    constructor() { }

    ngOnInit() {
        this.state = "toRedeem";
    }
}
