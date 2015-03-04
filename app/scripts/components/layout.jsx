var React = require('react');
var Router = require('react-router');
var RouteHandler = Router.RouteHandler;
var Navbar = require('./navbar')

// This layout is used by React-Router to layout the base container of the app
var Layout = React.createClass({

  render: function() {
    return (
      <div>
        <Navbar />
        <div id="app container">
          <RouteHandler />
        </div>
      </div>
    );
  }
});

module.exports = Layout;
