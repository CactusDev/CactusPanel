import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { LoginComponent } from "./login/login.component";
import { BeamComponent } from "./auth/beam/beam.component";
import { HomeComponent } from "./home/home.component";
import { CommandComponent } from "./command/command.component";
import { QuoteComponent } from "./quote/quote.component";
import { AlertComponent } from "./alert/alert.component";

const appRoutes: Routes = [
    { path: "login", component: LoginComponent },
    { path: "auth/beam/callback", component: BeamComponent},
    { path: "command", component: CommandComponent },
    { path: "dashboard", component: HomeComponent },
    { path: "quote", component: QuoteComponent },
    { path: "alert", component: AlertComponent },
    { path: "", redirectTo: "/dashboard", pathMatch: "full" },
    { path: "**", redirectTo: "/dashboard", pathMatch: "full" }
];

export const appRoutingProviders: any[] = [ ];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
