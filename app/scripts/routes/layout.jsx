import React from 'react';
import Reflux from 'reflux';
import { Grid } from 'react-bootstrap';
import { RouteHandlerMixin } from 'react-router';

import Navbar from './navbar';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), RouteHandlerMixin],

  getInitialState: function() {
    return {
      currentAuthor: null
    };
  },

  statics: {
    willTransitionTo: function (transition, params) {
      if (!AuthorStore.isLoggedIn()) {
        AuthorActions.checkAuth(transition);
      }
    }
  },

  render: function() {
    // we do this so we can pass essentially a global prop into the app in the
    // form of the currently logged in user
    // see http://stackoverflow.com/questions/27864720/react-router-pass-props-to-handler-component
    var AppHandler = this.createChildRouteHandler({currentAuthor: this.state.currentAuthor});
    return (
      <Grid fluid={true}>
        <Navbar currentAuthor={this.state.currentAuthor} />
        <Grid>
          {AppHandler}
        </Grid>
      </Grid>
    );
  }
});
