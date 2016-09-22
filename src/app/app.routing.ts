import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { CommandComponent } from "./command/command.component";
import { NotFoundComponent } from "./error/notfound.component";

const appRoutes: Routes = [
    { path: "command", component: CommandComponent },
    { path: "dashboard", component: HomeComponent },
    { path: "", redirectTo: "/dashboard", pathMatch: "full" },
    { path: "**", component: NotFoundComponent }
];

export const appRoutingProviders: any[] = [ ];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
