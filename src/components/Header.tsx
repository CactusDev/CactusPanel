
import * as React from "react";

import AppBar from "material-ui/AppBar";

import Drawer from "material-ui/Drawer";
import MenuItem from 'material-ui/MenuItem';
import Subheader from "material-ui/Subheader";
import { List, ListItem } from "material-ui/List";
import * as MatIcons from "material-ui/svg-icons";

import * as classnames from "classnames";

import { Link } from "react-router-dom";

export class Header extends React.Component {

    state = {
        navOpen: false
    }

    toggle = () => {
        this.setState({ navOpen: !this.state.navOpen });
    }

    close = () => {
        this.setState({ navOpen: false });
    }

    public render() {
        return (
            <div>
                <AppBar title="CactusBot Control Panel" onLeftIconButtonTouchTap={this.toggle}
                        className={classnames("navigation_bar", { expanded: this.state.navOpen })}/>

                <Drawer docked={true} open={this.state.navOpen} onRequestChange={(open) => this.setState({open})}
                        className="navigation_container">

                    <div className="center_contents">
                        <h3>Navigation</h3>
                    </div>

                    <Link to="/"><MenuItem primaryText="Dashboard"
                            leftIcon={<MatIcons.NavigationApps />} />
                    </Link>
                    <Link to="/commands"><MenuItem primaryText="Commands"
                        leftIcon={<MatIcons.NotificationPriorityHigh />} />
                    </Link>
                    <MenuItem primaryText="Quotes"
                            leftIcon={<MatIcons.CommunicationChat />} />
                    <MenuItem primaryText="Chat Alerts"
                            leftIcon={<MatIcons.CommunicationMessage />} />
                    <MenuItem primaryText="Settings"
                            leftIcon={<MatIcons.ActionSettings />} />
                </Drawer>
                {
                    <div className={classnames("content", { expanded: this.state.navOpen })}>
                        {
                            this.props.children
                        }
                    </div>
                }
            </div>
        );
    }
}
