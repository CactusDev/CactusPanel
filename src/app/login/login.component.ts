import { Component, OnInit } from "@angular/core";
import { Location } from "@angular/common";

// const Beam = require("beam-client-node");

import { Config } from "./../../../oauthConfig";

let config = new Config().getConfig();

@Component({
    selector: "app-root",
    template: ``
})

export class LoginComponent implements OnInit {

    constructor(private location: Location) { }

    ngOnInit() {
        // let client = new Beam();

        // client.use("oauth", {
        //     clientId: config.client.id,
        //     secret: config.client.secret
        // });

        // let url = client.getProvider().getRedirect("/auth/callback/beam", ["chat:connect"]);

        this.location.go("/dashboard");
    }
}
