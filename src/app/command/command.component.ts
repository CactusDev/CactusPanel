import { Component, OnInit } from "@angular/core";

@Component({
    selector: "app-root",
    templateUrl: "./command.component.html",
    styleUrls: ["command.component.less"]
})
export class CommandComponent implements OnInit {

    ngOnInit() {
        console.log("Potato salad");
    }

    constuctor() { }
}
