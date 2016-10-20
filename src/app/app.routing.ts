import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { SupportComponent } from "./support/support.component";
import { CodeComponent } from "./code/code.component";
import { HomeComponent } from "./home/home.component";
import { CommandComponent } from "./command/command.component";
import { QuoteComponent } from "./quote/quote.component";
import { AlertComponent } from "./alert/alert.component";

const appRoutes: Routes = [
    { path: "support", component: SupportComponent },
    { path: "command", component: CommandComponent },
    { path: "dashboard", component: HomeComponent },
    { path: "quote", component: QuoteComponent },
    { path: "alert", component: AlertComponent },
    { path: "code", component: CodeComponent },
    { path: "", redirectTo: "/dashboard", pathMatch: "full" },
    { path: "**", redirectTo: "/dashboard", pathMatch: "full" }
];

export const appRoutingProviders: any[] = [ ];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
