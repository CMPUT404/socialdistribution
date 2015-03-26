import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { Col, Button } from 'react-bootstrap';

import PostStore from '../../stores/post';
import PostActions from '../../actions/post';

import ContentViewer from '../content/content-viewer';
import Spinner from '../spinner';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Reflux.connect(PostStore)],

  getInitialState: function() {
    return {
      publicPosts: null
    };
  },

  componentDidMount: function() {
    this.refresh();
  },

  refresh: function() {
    PostActions.getPublicPosts();
  },

  render: function() {
    if (_.isNull(this.state.publicPosts)) {
      return (<Spinner />);
    }

    return (
      <Col md={8} mdOffset={2}>
        <h3>Recent Posts:<Button className="badge pull-right" onClick={this.refresh} type="submit">Refresh</Button></h3>
        <ContentViewer currentAuthor={this.props.currentAuthor} posts={this.state.publicPosts} />
      </Col>
    );
  }
});
