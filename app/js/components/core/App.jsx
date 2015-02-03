var React = require('react');
var Router = require('react-router');

var RouteHandler = Router.RouteHandler;

var App = React.createClass({
    render: function() {
        return (
            <div className="App">
                <div className="container-fluid">
                    <RouteHandler/>
                </div>
            </div>
        );
    }
});

module.exports = App;
