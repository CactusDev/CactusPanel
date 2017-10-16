
import * as React from "react";

import { Drawer } from "react-toolbox/lib/drawer";
import { Button } from "react-toolbox/lib/button";

export class Navigation extends React.Component {
    state = {
        active: false,
    };

    toggle = () => {
        this.setState({ active: !this.state.active });
    }

    render() {
        return (
            <div>
                <Button label="Show Navigation" raised accent onClick={this.toggle} />
                <Drawer active={this.state.active} onOverlayClick={this.toggle} className="navigation_container">
                    <h3>Navigation</h3>

                    <Button raised accent label="Dashboard" className="navigation_button" />
                    <Button raised accent label="Commands" className="navigation_button" />
                    <Button raised accent label="Quotes" className="navigation_button" />
                    <Button raised accent label="Event Alerts" className="navigation_button" />
                    <Button raised accent label="Settings" className="navigation_button" />
                </Drawer>
            </div>
        );
    }
}
