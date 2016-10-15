import { Component, OnInit } from "@angular/core";

@Component({
    selector: "app-root",
    templateUrl: "./command.component.html",
    styleUrls: ["command.component.less"]
})
export class CommandComponent implements OnInit {

    showControls: boolean = false;
    isVisible: string = "visibility";

    ngOnInit() { }

    toggleControls() {
        this.showControls = !this.showControls;
    }

    toggleEnabled() {
        if (this.isVisible === "isVisible") {
            this.isVisible = "visibility_off";
        } else {
            this.isVisible = "visibility";
        }
    }

    constuctor() { }
}
