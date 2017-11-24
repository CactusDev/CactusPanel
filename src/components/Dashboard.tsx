
import * as React from "react";

import RaisedButton from "material-ui/RaisedButton";
import AppBar from "material-ui/AppBar";

import Drawer from "material-ui/Drawer";
import MenuItem from 'material-ui/MenuItem';
import Subheader from "material-ui/Subheader";
import { List, ListItem } from "material-ui/List";
import * as MatIcons from "material-ui/svg-icons";

import * as classnames from "classnames";

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

export class Dashboard extends React.Component {

    public render() {
        return (
            <div>
                This is a dank dashboard!
            </div>
        );
    }
}
