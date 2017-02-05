var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery')
var Panel = require('react-bootstrap/lib/Panel');

class UserInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'name': null,
            'email': null,
        };
    }

    componentDidMount() {
        console.log("user-info did mount");
        $.ajax({
            url: "api/users/1",
            dataType: 'json',
            success: function(data) {
                console.log("user-info result received: " + JSON.stringify(data))
                this.setState(data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error("user-info error received", status, err.toString());
            }.bind(this)
        });
    }

    render() {
        if (this.state['name'] === null) {
            console.log("Rendering default user-info");
            return (
                <Panel header="User information" bsStyle="primary">
                    Loading...
                </Panel>
            );
        } else {
            console.log("Loaded user-info");
            return (
                <Panel header="User information" bsStyle="primary">
                    {this.state['name']} ({this.state['email']})
                </Panel>
            );
        }
    }
}

module.exports = UserInfo
