import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { State } from 'react-router';
import { Col } from 'react-bootstrap';

import PostStore from '../stores/post';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';
import ContentViewer from './contentviewer';
import ContentCreator from './contentcreator';

// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

mixins: [Reflux.connect(AuthorStore), Reflux.connect(PostStore), State],

  getInitialState: function() {
    return {
      displayAuthor: {},
      posts: []
    };
  },

  componentDidMount: function () {
    AuthorActions.getAuthorViewData(this.getParams().id);
  },

  render: function() {
    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorViewId = this.getParams().id;
    var contentCreator;

    // if the logged in author is trying to view his own page
    if (
      !Check.emptyObject(this.props.currentAuthor) &&
      this.props.currentAuthor.id == authorViewId
    ) {
      contentCreator = <ContentCreator currentAuthor={this.props.currentAuthor} />;
    }

    return (
      <Col md={12}>
        <div className="media well author-biography">
          <div className="media-left">
            <img className="media-object profile-image" src={this.state.displayAuthor.image} />
          </div>
          <div className="media-body">
            <h4 className="media-heading">{this.state.displayAuthor.name}</h4>
            <p><strong>Bio:</strong> {this.state.displayAuthor.bio}</p>
            <p><a href={this.state.displayAuthor.github} target="_blank">Github</a></p>
          </div>
        </div>
        <div className="jumbotron">
        {contentCreator}
        </div>
        <ContentViewer
          currentAuthor={this.props.currentAuthor}
          posts={this.state.posts} />
      </Col>
    );
  }
});
