import _ from 'lodash';
import React from 'react';
import { Col, Button } from 'react-bootstrap';

import PostActions from '../actions/post';

import ContentViewer from './contentviewer';
import Spinner from './spinner';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  getInitialState: function() {
    return {
      posts: null
    };
  },

  componentDidMount: function() {
    this.refresh();
  },

  refresh: function () {
    // PostActions.publicposts...
  },

  render: function() {
    if (_.isNull(this.state.posts)) {
      return (<Spinner />);
    }

    return (
      <Col md={12}>
        <h3>Recent Posts:<Button className="badge pull-right" onClick={this.refresh} type="submit">Refresh</Button></h3>
        <ContentViewer currentAuthor={this.props.currentAuthor} posts={this.state.posts} />
      </Col>
    );
  }
});
