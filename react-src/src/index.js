var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery')

class App extends React.Component {
    render() {
        return (
            <div className="app">
                <UserInfo />
            </div>
        );
    }
};

class UserInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'name': null,
            'email': null,
        };
    }

    componentDidMount() {
        $.ajax({
            url: "api/users/1",
            dataType: 'json',
            success: function(data) {
                this.setState(data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    }

    render() {
        if (this.state['name'] === null) {
            return (
                <div class="userinfo">
                    <div><b>User information</b></div>
                    Loading...
                </div>
            );
        } else {
            return (
                <div class="userinfo">
                    <div><b>User information</b></div>
                    {this.state['name']} ({this.state['email']})
                </div>
            );
        }
    }
}

loadApp = function(elementId) {
    ReactDOM.render(
        <App />,
        document.getElementById(elementId)
    );
};
