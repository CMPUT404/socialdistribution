import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { Col, Button } from 'react-bootstrap';
import { State, Navigation } from 'react-router';

import PostStore from '../stores/post';
import PostActions from '../actions/post';
import UserSearch from './usersearch';
import ContentCreator from './contentcreator';
import ContentViewer from './contentviewer';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Reflux.connect(PostStore), State, Navigation],

  getInitialState: function() {
    return {
      timeline: []
    };
  },

  componentDidMount: function () {
    this.refresh();
  },

  refresh: function () {
    PostActions.getTimeline(this.props.currentAuthor.id);
  },

  render: function() {
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
