var React = require('react');
var ReactDOM = require('react-dom');

class Tracker extends React.Component {
    render() {
        return (
            <div className="tracker">
                Tracker goes here!
            </div>
        );
    }
};

loadTracker = function(elementId) {
    ReactDOM.render(
        <Tracker />,
        document.getElementById(elementId)
    );
};
