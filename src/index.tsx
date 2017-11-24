import * as React from "react";
import * as ReactDOM from "react-dom";

import { Header } from "./components/Header";
import { Dashboard } from "./components/Dashboard";
import { Commands } from "./components/Commands";
import { Setup } from "./components/Setup";

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import * as Colors from 'material-ui/styles/colors';

import { HashRouter, Route, Link, Switch } from "react-router-dom";

const theme = getMuiTheme({
    palette: {
        accent1Color: Colors.purple700,
        primary1Color: Colors.green400
    }
});

ReactDOM.render(
    <div>
        <MuiThemeProvider muiTheme={theme}>
            <HashRouter>
                <div>
                    <Header>
                        <div className="content">
                            <Switch>
                                <Route exact path="/" component={Dashboard} />
                                <Route path="/commands" component={Commands} />
                                <Route path="/setup" component={Setup} />
                            </Switch>
                        </div>
                    </Header>
                </div>
            </HashRouter>
        </MuiThemeProvider>
    </div>,
    document.getElementById("app"));