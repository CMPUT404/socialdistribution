import React from 'react';
import Navbar from './navbar';
import { Grid, Col } from 'react-bootstrap';
import { default as Router, RouteHandler} from 'react-router';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore, "currentAuthor")],

  getInitialState: function () {
    return {
      currentAuthor: {}
    };
  },

  componentDidMount: function () {
    AuthorActions.refreshCurrentAuthor();
  },

  render: function() {
    return (
      <Grid fluid={true}>
        <Navbar author={this.state.currentAuthor} />
        <Grid>
          <Col md={8} mdOffset={2}>
            <RouteHandler author={this.state.currentAuthor} />
          </Col>
        </Grid>
      </Grid>
    );
  }
});
