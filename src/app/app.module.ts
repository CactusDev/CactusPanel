import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { AppComponent } from "./app.component";

import { SidebarComponent } from "./sidebar/sidebar.component";

import { CodeComponent } from "./code/code.component";
import { HomeComponent } from "./home/home.component";
import { CommandComponent } from "./command/command.component";
import { QuoteComponent } from "./quote/quote.component";
import { AlertComponent } from "./alert/alert.component";

import { routing, appRoutingProviders } from "./app.routing";

import { MaterialModule } from "@angular/material";

@NgModule({
  declarations: [
      AppComponent,
      CodeComponent,
      HomeComponent,
      CommandComponent,
      QuoteComponent,
      SidebarComponent,
      AlertComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    routing
  ],
  providers: [
    appRoutingProviders
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
