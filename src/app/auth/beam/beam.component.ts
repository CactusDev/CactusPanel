import { Component, OnInit } from "@angular/core";

const passport = require("passport");

@Component({
    selector: "app-root",
    template: ``
})

export class BeamComponent implements OnInit {
    ngOnInit() {
        // passport.authenticate("beam", {
        //     successRedirect: "/dashboard",
        //     failureRedirerct: "/login"
        // });
    }
}
