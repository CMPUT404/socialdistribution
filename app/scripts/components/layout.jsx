import React from 'react';
import Navbar from './navbar';
import { Grid, Col } from 'react-bootstrap';
import { RouteHandler } from 'react-router';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
export default React.createClass({

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
