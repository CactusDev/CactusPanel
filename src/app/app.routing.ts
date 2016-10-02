import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { CommandComponent } from "./command/command.component";
import { QuoteComponent } from "./quote/quote.component";

const appRoutes: Routes = [
    { path: "command", component: CommandComponent },
    { path: "dashboard", component: HomeComponent },
    { path: "quote", component: QuoteComponent },
    { path: "", redirectTo: "/dashboard", pathMatch: "full" },
    { path: "**", redirectTo: "/dashboard", pathMatch: "full" }
];

export const appRoutingProviders: any[] = [ ];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
