
import * as React from "react";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";
import TextField from "material-ui/TextField";
import DropDownMenu from "material-ui/DropDownMenu";
import MenuItem from "material-ui/MenuItem";

const styles = {
	container: {
		display: "flex"
	},
	name: {
		width: "20%",
		marginRight: "10px"
	},
	response: {
		width: "80%"
	},
	roles: {
		width: "40%",
		padding: "0px",
		margin: "0px"
	},
	rolesContainer: {
		display: "flex",
		justifyContent: "center",
		alignItems: "center",
		// width: "20%"
	}
}

export default class CommandCreateModal extends React.Component {

	private items: any[];

	constructor(public props: any) {
		super(props);

		let items: any[] = [];

		for (let key of Object.keys(this.props.items)) {
			const item = this.props.items[key];

			items.push(<MenuItem value={item.power} key={item.power} primaryText={key} />);
		}

		this.items = items;
		this.state = { value: this.props.items[Object.keys(this.props.items)[0]].power };
	}

	state = {
		value: ""
	}

	handleChange = (event: any, index: any, value: any) => {
		this.setState({ value });
	}

	public render() {
		const actions: any[] = [
			<FlatButton 
				label="Cancel"
				primary={true}
				onClick={this.props.cancel}
			/>,
			<FlatButton 
				label="Create"
				primary={true}
				onClick={this.props.create}
			/>
		];

		return (
			<div>
				<Dialog
					title="Create a New Command"
					actions={actions}
					modal={true}
					open={this.props.open}
				>
					<div style={styles.container}>
						<TextField hintText="Command Name" floatingLabelText="Command Name" style={styles.name}></TextField>
						<TextField hintText="Command Response" floatingLabelText="Command Response" multiLine={true} style={styles.response}></TextField>
					</div>

					<div style={styles.rolesContainer}>
						<DropDownMenu maxHeight={300} autoWidth={false} value={this.state.value}
									  onChange={this.handleChange} style={styles.roles}>
							{this.items}
						</DropDownMenu>
					</div>
				</Dialog>
			</div>
		)	
	}
}
