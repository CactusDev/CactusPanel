import * as React from "react";
import * as ReactDOM from "react-dom";

import { Header } from "./components/Header";
import { Dashboard } from "./components/Dashboard";
import { Commands } from "./components/Commands";

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import * as Colors from 'material-ui/styles/colors';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const theme = getMuiTheme({
    palette: {
        accent1Color: Colors.purple700,
        primary1Color: Colors.green400
    }
})

ReactDOM.render(
    <div>
        <MuiThemeProvider muiTheme={theme}>

            <Router>
                <div>
                    <Header>
                        <div className="content">
                            <Route exact path="/" component={Dashboard} />
                            <Route exact path="/commands" component={Commands} />
                        </div>
                    </Header>
                </div>
            </Router>
        </MuiThemeProvider>
    </div>,
    document.getElementById("app"));