import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { State } from 'react-router';
import { Col } from 'react-bootstrap';

import PostStore from '../stores/post';
import AuthorStore from '../stores/author';
import ContentViewer from './contentviewer';
import ContentCreator from './contentcreator';

// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), State],

  getInitialState: function() {
    return {
      currentAuthor: {},
      displayAuthor: {}
    };
  },

  componentDidMount: function () {
    AuthorActions.getAuthorViewData(this.getParams().id);
  },

  render: function() {
    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorViewId = this.getParams().id;
    var currentAuthor = this.state.currentAuthor;
    var profile = false, contentCreator;

    // if the logged in author is trying to view his own page
    if (Check.object(this.state.currentAuthor) && authorViewId == this.state.currentAuthor.id) {
      contentCreator = <ContentCreator author={this.state.currentAuthor} />;
      profile = true;
    }

    return (
      <Col md={12}>
        <div className="media">
          <div className="media-left">
            <img className="media-object profile-image" src={this.state.displayAuthor.author_image} />
          </div>
          <div className="media-body">
            <h4 className="media-heading">{this.state.displayAuthor.name}</h4>
            <p>{this.state.displayAuthor.bio}</p>
          </div>
        </div>
        <div className="jumbotron">
        {contentCreator}
        </div>
        <ContentViewer currentAuthor={author} authorViewId={authorViewId} isProfile={profile} />
      </Col>
    );
  }
});
