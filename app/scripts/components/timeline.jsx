import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { Col, Button } from 'react-bootstrap';
import { State, Navigation } from 'react-router';

import PostStore from '../stores/post';
import AuthorStore from '../stores/author';
import PostActions from '../actions/post';
import UserSearch from './usersearch';
import ContentCreator from './contentcreator';
import ContentViewer from './contentviewer';

import Spinner from './spinner';


// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Reflux.connect(PostStore), State, Navigation],

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

  componentDidMount: function () {
    this.refresh();
  },

  refresh: function () {
    // PostActions.getTimeline(this.props.currentAuthor.id);
  },

  shouldComponentUpdate: function(nextProps) {
    // When an author logs out we want to make sure that we
    // kick them out of the timeline page
    // And redirect them back to the login page
    if (_.isNull(nextProps.currentAuthor)) {
      this.transitionTo('login');
      return false;
    }

    return true;
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
