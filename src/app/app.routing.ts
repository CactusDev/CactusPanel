import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './home/app.component';
import { CommandComponent } from './command/command.component';
import { NotFoundComponent } from './error/notfound.component';

const appRoutes: Routes = [
    { path: 'commands', component: CommandComponent },
    { path: 'dashboard', component: AppComponent },
    { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
    { path: '**', component: NotFoundComponent }
];

export const appRoutingProviders: any[] = [

];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
