
import * as React from "react";

import RaisedButton from "material-ui/RaisedButton";
import FlatButton from "material-ui/FlatButton";
import AppBar from "material-ui/AppBar";
import Toggle from "material-ui/Toggle";
import { Step, Stepper, StepLabel } from 'material-ui/Stepper';
import { List, ListItem } from "material-ui/List";
import TextField from 'material-ui/TextField';

import * as MatIcons from "material-ui/svg-icons";

const styles = {
    trackSwitchedTwitch: {
        backgroundColor: "#6441A4"
    },
    thumbSwitchedTwitch: {
        backgroundColor: "#7b50c9"
    },
    trackSwitchedMixer: {
        backgroundColor: "#1FBAED"
    },
    thumbSwitchedMixer: {
        backgroundColor: "#21c8ff"
    }
}

export class Setup extends React.Component {

    private totalSteps = 3;

    state = {
        finished: false,
        stepIndex: 0,
        accountCreated: false
    }

    next = () => {
        const { stepIndex } = this.state;
        
        this.setState({
            stepIndex: stepIndex + 1,
            finished: stepIndex >= this.totalSteps
        });
    }

    back = () => {
        const {stepIndex} = this.state;

        if (stepIndex > 0) {
            this.setState({ stepIndex: stepIndex - 1 });
        }
    }

    createAccount = () => {
        this.setState({ accountCreated: true });
    }

    getStepContent(index: number) {
        switch (index) {
            case 0:
                return (
                    <div>
                        <h3>What platforms do you stream on?</h3>

                        <Toggle label="Twitch" labelPosition="right"
                            trackSwitchedStyle={styles.trackSwitchedTwitch}
                            thumbSwitchedStyle={styles.thumbSwitchedTwitch} />
                        
                        <Toggle label="Mixer" labelPosition="right"
                                trackSwitchedStyle={styles.trackSwitchedMixer}
                                thumbSwitchedStyle={styles.thumbSwitchedMixer} />
                    </div>
                );
            case 1:
                return (
                    <div>
                        <h3>What account would you like to use?</h3>

                        <p>You don't get to choose at this moment in time</p>
                        <p>Currently, you're restricted to the account 'CactusBotBeta'</p>
                    </div>
                );
            case 2:
                return (
                    <div>
                        <h3>Account Setup</h3>

                        <TextField errorText="Must provide a username" hintText="Username" floatingLabelText="Username" fullWidth />
                        <TextField errorText="Must provide a password" hintText="Password" floatingLabelText="Password" type="password" fullWidth />
                    </div>
                );
            case 3:
                return (
                    <div className="center_contents">
                        <RaisedButton disabled={this.state.accountCreated} label="Create Account" secondary icon={<MatIcons.ActionAccountCircle />} onClick={this.createAccount} fullWidth className="stepped_button" />
                        <RaisedButton disabled={!this.state.accountCreated} label="Join Channel" secondary icon={<MatIcons.ActionLaunch />} fullWidth className="stepped_button" />
                    </div>
                );
        }
    }

    public render() {
        const {finished, stepIndex} = this.state;
        const contentStyle = {margin: '0 16px'};
    
        return (
          <div style={{width: "100%", maxWidth: "50%", margin: "auto"}}>
            <Stepper activeStep={stepIndex}>
                <Step>
                    <StepLabel>Platforms</StepLabel>
                </Step>
                
                <Step>
                    <StepLabel>Bot Account</StepLabel>
                </Step>
                
                <Step>
                    <StepLabel>Account Setup</StepLabel>
                </Step>
                
                <Step>
                    <StepLabel>Finalize</StepLabel>
                </Step>
            </Stepper>

            <div style={contentStyle}>
              {finished ? (
                <p>All setup!</p>
              ) : (
                <div>
                  {this.getStepContent(stepIndex)}
                  <div style={{marginTop: 12}}>
                    <FlatButton
                      label="Back"
                      disabled={stepIndex === 0}
                      onClick={this.back}
                      style={{marginRight: 12}}
                    />
                    <RaisedButton
                      label={stepIndex === this.totalSteps ? 'Finish' : 'Next'}
                      primary={true}
                      onClick={this.next}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        );
    }
}
