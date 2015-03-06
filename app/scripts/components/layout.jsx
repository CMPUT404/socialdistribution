var React = require('react');
var Router = require('react-router');
var RouteHandler = Router.RouteHandler;
var Navbar = require('./navbar')
import { Grid, Col } from 'react-bootstrap';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
var Layout = React.createClass({

  render: function() {
    return (
      <Grid fluid={true}>
        <Navbar />
        <Grid>
          <Col md={8} mdOffset={2}>
            <RouteHandler />
          </Col>
        </Grid>
      </Grid>
    );
  }
});

module.exports = Layout;
