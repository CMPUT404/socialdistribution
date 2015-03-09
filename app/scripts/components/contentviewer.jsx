import React from 'react';

import ContentCreator from './contentcreator';
import Content from './content';

// This is used to bundle up user content we wish to display. Namely posts and
// comments. It listens to and updates based on changes in the Post Store.
export default React.createClass({

  render: function() {
    var posts = [];

    // create an array of posts or comments
    this.props.posts.forEach(function (post, id) {
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
            <ContentCreator key="comment-creator" currentAuthor={currentAuthor} post={post} forComment={true} />
          </div>
        </div>
      );
    });

    return (
      <div className="content-viewer well">
        {posts}
      </div>
    );
  }
});
