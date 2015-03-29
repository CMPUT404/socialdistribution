import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { Col, Button } from 'react-bootstrap';
import { Navigation } from 'react-router';

import AuthorActions from '../actions/author';
import PostActions from '../actions/post';

import PostCreator from '../components/content/post-creator';
import ContentViewer from '../components/content/content-viewer';
import Spinner from '../components/spinner';

import AuthorStore from '../stores/author';
import PostStore from '../stores/post';

import ActionListener from '../mixins/action-listener';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Reflux.connect(PostStore), Navigation, ActionListener],

  statics: {
    willTransitionTo: function (transition, params) {
      if (!AuthorStore.isLoggedIn()) {
        transition.redirect('login');
      }
    }
  },

  getInitialState: function() {
    return {
      timeline: null
    };
  },

  componentDidMount: function() {
    // Listen to logout then transition
    this.listen(AuthorActions.logout, () => this.transitionTo('login'));
    // refresh posts?
    this.refresh();
  },

  refresh: function() {
    PostActions.getTimeline(this.props.currentAuthor.token);
  },

  render: function() {
    if (_.isNull(this.state.timeline)) {
      return (<Spinner />);
    }

    return (
      <Col md={8} mdOffset={2}>
        <div className="jumbotron">
          <h3>Mood?</h3>
          <PostCreator currentAuthor={this.props.currentAuthor} />
        </div>
        <h3>Recent Posts:<Button className="badge pull-right" onClick={this.refresh} type="submit">Refresh</Button></h3>
        <ContentViewer currentAuthor={this.props.currentAuthor} posts={this.state.timeline} />
      </Col>
    );
  }
});
