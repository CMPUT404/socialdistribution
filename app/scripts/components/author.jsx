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
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  render: function() {
    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorId = this.getParams().authorId;
    var currentAuthor = this.state.currentAuthor;
    var profile = false, contentCreator;

    // if the logged in author is trying to view his own page
    if (Check.object(currentAuthor) && authorId == currentAuthor.id) {
      contentCreator = <ContentCreator authorId={authorId} />;
      profile = true;
    }

    return (
      <Col md={12}>
        {contentCreator}
        <ContentViewer authorId={authorId} isProfile={profile} />
      </Col>
    );
  }
});
