import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { Grid, Col } from 'react-bootstrap';
import { State, Navigation } from 'react-router';
import RouteHandler from 'react-router/modules/mixins/RouteHandler';

import Navbar from './navbar';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
export default React.createClass({

  mixins: [Reflux.listenTo(AuthorStore, "checkAuthResult"), State, Navigation, RouteHandler],

  getInitialState: function() {
    return {
      currentAuthor: {}
    };
  },

  checkAuthResult: function(state) {
    // on successful login, set logged in state and transition to base timeline
    if (Check.object(state.currentAuthor)) {
      this.setState({currentAuthor: state.currentAuthor});
      this.transitionTo('timeline');
    // otherwise ensure the user is at the login view if not already
    } else if(!this.isActive('login')) {
      this.transitionTo('login');
    }
  },

  // As soon as our base layout is ready, figure out if the user is logged in
  componentDidMount: function () {
    AuthorActions.checkAuth();
  },

  render: function() {

    // we do this so we can pass essentially a global prop into the app in the
    // form of the currently logged in user
    // see http://stackoverflow.com/questions/27864720/react-router-pass-props-to-handler-component
    var AppHandler = this.getRouteHandler({currentAuthor: this.state.currentAuthor});
    return (
      <Grid fluid={true}>
        <Navbar author={this.state.currentAuthor} />
        <Grid>
          <Col md={8} mdOffset={2}>
            {AppHandler}
          </Col>
        </Grid>
      </Grid>
    );
  }
});
