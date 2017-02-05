var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');
var Panel = require('react-bootstrap/lib/Panel');
var UserInfo = require('./userinfo');
var DailyLog = require('./dailylog');

class App extends React.Component {
    render() {
        return (
            <div className="app">
                <UserInfo />
                <DailyLog />
            </div>
        );
    }
};

loadApp = function(elementId) {
    ReactDOM.render(
        <App />,
        document.getElementById(elementId)
    );
};
