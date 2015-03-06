import React from 'react';
import Reflux from 'reflux';
import Content from './content';
import { Button } from 'react-bootstrap';
import ContentCreator from './contentcreator';

import PostStore from '../stores/post';
import PostActions from '../actions/post';

// This is used to bundle up user content we wish to display. Namely posts and
// comments. It listens to and updates based on changes in the Post Store.
export default React.createClass({

  mixins: [Reflux.connect(PostStore)],

  getInitialState: function() {
    return { posts: new Map() };
  },

  // when the component is loaded in the browser this is called automatically
  // and fetches posts asynchronously in the background
  componentDidMount: function() {
    this.refresh();
  },

  refresh: function() {
    var query = {author_id: this.props.authorId, author_only: false};
    if (this.props.isProfile) {
      query.author_only = true;
    }

    PostActions.refreshPosts(query);
  },

  render: function() {
    var posts = [];

    // create an array of posts or comments
    this.state.posts.forEach(function (post, id) {
      posts.push(
                <div className="panel panel-default" key={id}>
                  <div className="panel-body">
                    <ul className="media-list">
                      <li className="media">
                        <Content data={post} isPost={true} />
                      </li>
                    </ul>
                  </div>
                  <div className="panel-footer">
                    <ContentCreator key="comment-creator" post={post} forComment={true} />
                  </div>
                </div>
                );
    });

    return (
      <div className="content-viewer well">
        <h3>Recent Posts:<Button className="badge pull-right" onClick={this.refresh} type="submit">Refresh</Button></h3>
        {posts}
      </div>
    );
  }
});
