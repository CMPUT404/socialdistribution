import React from 'react';
import Reflux from 'reflux';
import { Grid } from 'react-bootstrap';
import RouteHandler from 'react-router/modules/mixins/RouteHandler';

import Navbar from './navbar';
import AuthorActions from '../actions/author';

import ActionListener from '../mixins/action-listener';

// This layout is used by React-Router to layout the base container of the app.
// We shouldn't really be putting anything here other than the Navbar.
export default React.createClass({

  mixins: [RouteHandler, ActionListener],

  getInitialState: function() {
    return {
      currentAuthor: null
    };
  },

  // As soon as our base layout is ready, figure out if the user is logged in
  componentDidMount: function () {
    var self = this;
    var complete = (a) => this.setState({currentAuthor: a});

    // Way more efficient than listening for every change from author store
    this.listen(AuthorActions.logout, () => this.setState(this.getInitialState()));
    this.listen(AuthorActions.checkAuth.complete, complete);
    this.listen(AuthorActions.login.complete, complete);

    AuthorActions.checkAuth();
  },

  render: function() {
    // we do this so we can pass essentially a global prop into the app in the
    // form of the currently logged in user
    // see http://stackoverflow.com/questions/27864720/react-router-pass-props-to-handler-component
    var AppHandler = this.getRouteHandler({currentAuthor: this.state.currentAuthor});
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
