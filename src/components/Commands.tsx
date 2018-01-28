
import * as React from "react";

import FlatButton from "material-ui/FlatButton"
import * as MatIcons from "material-ui/svg-icons";
import FloatingActionButton from "material-ui/FloatingActionButton";
import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn
} from "material-ui/Table"
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';

interface Command {
    name: string;
    response: string;
    role: string;
}

export class Commands extends React.Component {

    private getCommands(channel: string): Command[] {
        return [
            {
                name: "a",
                response: "Dank testing command",
                role: "user"
            },
            {
                name: "b",
                response: "This is a moderator command",
                role: "moderator"
            },
            {
                name: "c",
                response: "This is a sub command",
                role: "subscriber"
            }
        ];
    }

    public render() {
        let content: any[] = [];

        this.getCommands("innectic").forEach(command => {
            let icon: any = <MatIcons.SocialPerson />;
            if (command.role === "moderator") {
                icon = <MatIcons.HardwareSecurity />;
            } else if (command.role === "subscriber") {
                icon = <MatIcons.EditorAttachMoney />;
            }

            content.push(
                <TableRow>
                    <TableHeaderColumn style={{ width: "5%" }}>{icon}</TableHeaderColumn>
                    <TableRowColumn style={{ width: "15%" }}>{command.name}</TableRowColumn>
                    <TableRowColumn>
                        <div className="command_response">{command.response}</div>
                        <span className="command_extras">
                            <IconMenu iconButtonElement={
                              <IconButton><MatIcons.NavigationMoreVert /></IconButton>
                            }>
                                <MenuItem primaryText="Edit" />
                                <MenuItem primaryText="Delete" />
                            </IconMenu>
                        </span>
                    </TableRowColumn>
                </TableRow>
            );
        });

        return (
            <div className="command_list_page content-width">
                <Table selectable={false} multiSelectable={false}>
                    <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
                        <TableRow>
                            <TableHeaderColumn style={{ width: "5%" }}>Role</TableHeaderColumn>
                            <TableHeaderColumn style={{ width: "15%" }}>Name</TableHeaderColumn>
                            <TableHeaderColumn>Response</TableHeaderColumn>
                        </TableRow>
                    </TableHeader>

                    <TableBody displayRowCheckbox={false}>
                        {content}
                    </TableBody>
                </Table>

                <div className="add_new_command_fab_button">
                    <FloatingActionButton>
                        <MatIcons.ContentAdd />
                    </FloatingActionButton>
                </div>
            </div>
        );
    }
}
