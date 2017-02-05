var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery')
var Button = require('react-bootstrap/lib/Button');
var ControlLabel = require('react-bootstrap/lib/ControlLabel');
var Form = require('react-bootstrap/lib/Form');
var FormControl = require('react-bootstrap/lib/FormControl');
var Panel = require('react-bootstrap/lib/Panel');

class DailyLog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'data': [],
            'addMode': 'showButtons'
        };

        this.doLoadData = this.doLoadData.bind(this);
        this.loadAndMergeMeals = this.loadAndMergeMeals.bind(this);
        this.handleData = this.handleData.bind(this);
        this.handleError = this.handleError.bind(this);
        this.showAddMeasurement = this.showAddMeasurement.bind(this);
        this.showAddMeal = this.showAddMeal.bind(this);
        this.showButtons = this.showButtons.bind(this);
    }

    componentDidMount() {
        console.log("DailyLog did mount");
        this.doLoadData(this.handleData.bind(this), this.handleError.bind(this));
    }

    doLoadData(onSuccess, onFailure) {
        $.ajax({
            url: "api/users/1/measurements",
            dataType: 'json',
            success: function(data) {
                console.log("DailyLog loaded " + data.length + " measurements");
                data.map(function(datum) {
                    datum['type'] = 'measurement';
                });
                this.loadAndMergeMeals(data, onSuccess, onFailure);
            }.bind(this),
            error: function(xhr, status, err) {
                onFailure("measurements", status, err.toString());
            }.bind(this)
        });
    }

    loadAndMergeMeals(measurements, onSuccess, onFailure) {
        $.ajax({
            url: "api/users/1/meals",
            dataType: 'json',
            success: function(data) {
                console.log("DailyLog loaded " + data.length + " meals");
                data.map(function(datum) {
                    datum['type'] = 'meal';
                });
                // TODO post-process
                onSuccess(measurements.concat(data));
            }.bind(this),
            error: function(xhr, status, err) {
                onFailure("meals", status, err.toString());
            }.bind(this)
        });
    }

    handleData(data) {
        console.log("DailyLog processing " + data.length + " total measurements");
        this.setState({'data': data});
    }

    handleError(call, status, errString) {
        console.log("DailyLog hit an error rendering " + call, status, err.toString());
    }

    render() {
        var logEntries = this.state.data.map(function (item) {
            if (item['type'] == 'measurement') {
                return (
                    <Measurement weight={item.weight} timestamp={item.timestamp} />
                );
            } else {
                return (
                    <Meal amount={item.amount} timestamp={item.timestamp} />
                );
            }
        });

        if (this.state.addMode == 'showButtons') {
            return (
                <Panel className="logEntryList" header="Daily log" bsStyle="success">
                    {logEntries}
                    <AddEntryButtonsPanel addMeasurementFn={this.showAddMeasurement} addMealFn={this.showAddMeal} />
                </Panel>
            );
        } else if (this.state.addMode == 'addMeasurement') {
            return (
                <Panel className="logEntryList" header="Daily log" bsStyle="success">
                    {logEntries}
                    <AddMeasurementPanel cancelFn={this.showButtons} reloadFn={this.doLoadData} />

                </Panel>
            );
        } else {
            return (
                <Panel className="logEntryList" header="Daily log" bsStyle="success">
                    {logEntries}
                    <AddMealPanel cancelFn={this.showButtons} reloadFn={this.doLoadData} />
                </Panel>
            );
        }
    }

    showButtons() {
        this.setState({
            'addMode': 'showButtons',
        });
    }

    showAddMeasurement() {
        this.setState({
            'addMode': 'addMeasurement',
        });
    }

    showAddMeal() {
        this.setState({
            'addMode': 'addMeal',
        });
    }
}

class Measurement extends React.Component {
    render() {
        return (
            <div className="logEntry">
                <b>Measurement</b> {this.props.timestamp}, {this.props.weight}g
            </div>
        );
    }
}

class Meal extends React.Component {
    render() {
        return (
            <div className="logEntry">
                <b>Meal</b> {this.props.timestamp}, {this.props.amount}g
            </div>
        );
    }
}

class AddEntryButtonsPanel extends React.Component {
    render() {
        return (
            <div>
                <Button
                        onClick={this.props.addMeasurementFn}
                        bsStyle="info">
                    Record weight
                </Button>
                <Button
                        onClick={this.props.addMealFn}
                        bsStyle="warning">
                    Add meal
                </Button>
            </div>
        );
    }
}

class AddMeasurementPanel extends React.Component {
    render() {
        return (
            <Form inline>
            <ControlLabel>MEASUREMENT</ControlLabel>
            <ControlLabel>Weight (grams)</ControlLabel>
            <FormControl type="text" />
            <Button bsStyle="primary" type="submit">Save</Button>
            <Button onClick={this.props.cancelFn} bsStyle="danger">Cancel</Button>
            </Form>
        );
    }
}

class AddMealPanel extends React.Component {
    render() {
        return (
            <Form inline>
            <ControlLabel>MEAL</ControlLabel>
            <ControlLabel>Amount (grams)</ControlLabel>
            <FormControl type="text" />
            <Button bsStyle="primary" type="submit">Save</Button>
            <Button onClick={this.props.cancelFn} bsStyle="danger">Cancel</Button>
            </Form>
        );
    }
}


module.exports = DailyLog
