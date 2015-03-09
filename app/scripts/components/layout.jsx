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
      currentAuthor: {},
      initialLoad: true // helper to avoid bug when devving
    };
  },

  checkAuthResult: function(state) {

    // only perform updates if our currentAuthor is being changed
    if (!Check.undefined(state.currentAuthor)) {

      // set state, then transition
      this.setState({currentAuthor: state.currentAuthor, initialLoad: false});

      if (Check.emptyObject(state.currentAuthor) && !this.isActive('login')) {
        this.transitionTo('login');
      } else {
        this.transitionTo('timeline');
      }
    }
  },

  // As soon as our base layout is ready, figure out if the user is logged in
  componentDidMount: function () {
    AuthorActions.checkAuth();
  },

  render: function() {

    if (Check.emptyObject(this.state.currentAuthor && this.state.intialLoad)) {
      return (<div></div>);
    }

    // we do this so we can pass essentially a global prop into the app in the
    // form of the currently logged in user
    // see http://stackoverflow.com/questions/27864720/react-router-pass-props-to-handler-component
    var AppHandler = this.getRouteHandler({currentAuthor: this.state.currentAuthor});
    return (
      <Grid fluid={true}>
        <Navbar currentAuthor={this.state.currentAuthor} />
        <Grid>
          <Col md={8} mdOffset={2}>
            {AppHandler}
          </Col>
        </Grid>
      </Grid>
    );
  }
});
