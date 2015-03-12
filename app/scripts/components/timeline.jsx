import _ from 'lodash';
import React from 'react';
import { Col, Button } from 'react-bootstrap';
import { Navigation } from 'react-router';

import AuthorActions from '../actions/author';
import PostActions from '../actions/post';

import ContentCreator from './contentcreator';
import ContentViewer from './contentviewer';
import UserSearch from './usersearch';
import Spinner from './spinner';

import AuthorStore from '../stores/author';

import ActionListener from '../mixins/action-listener';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Navigation, ActionListener],

  statics: {
    willTransitionTo: function (transition, params) {
      if (!AuthorStore.isLoggedIn()) {
        transition.redirect('login');
      }
    }
  },

  getInitialState: function() {
    return {
      // starts at null and if no reuslt it
      // return an empty array
      timeline: null
    };
  },

  componentDidMount: function() {
    // Listen to logout then transition
    this.listen(AuthorActions.logout, () => this.transitionTo('login'));
    // refresh posts?
    this.refresh();
  },

  refresh: function () {
    // PostActions.getTimeline(this.props.currentAuthor.id);
  },

  render: function() {
    if (_.isNull(this.state.timeline)) {
      return (<Spinner />);
    }

    return (
      <Col md={12}>
        <UserSearch key="search" />
        <div className="jumbotron">
          <h3>Mood?</h3>
          <ContentCreator currentAuthor={this.props.currentAuthor} />
        </div>
        <h3>Recent Posts:<Button className="badge pull-right" onClick={this.refresh} type="submit">Refresh</Button></h3>
        <ContentViewer currentAuthor={this.props.currentAuthor} posts={this.state.timeline} />
      </Col>
    );
  }
});
