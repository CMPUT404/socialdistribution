var React = require('react');
var Router = require('react-router');
var RouteHandler = Router.RouteHandler;

// This layout is used by React-Router to layout the base container of the app
var Layout = React.createClass({

  render: function() {
    return (
      <div className="container app">
        <RouteHandler />
      </div>
    );
  }
});

module.exports = Layout;
