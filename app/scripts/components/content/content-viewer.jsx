import _ from 'lodash';
import React from 'react';

import CommentCreator from './comment-creator';
import Content from './content';

import Spinner from '../spinner';

// This is used to bundle up user content we wish to display. Namely posts and
// comments. It listens to and updates based on changes in the Post Store.
export default React.createClass({

  render: function() {
    var posts = [];

    if (_.isNull(this.props.posts)) {
      return (<Spinner />);
    }

    // orders posts if any are passed in as props
    if (this.props.posts.length > 0) {
      for (let post of this.props.posts) {
        posts.push(
          <div className="panel panel-default" key={"post-"+post.guid}>
            <div className="panel-body">
              <ul className="media-list">
                <li className="media">
                  <Content data={post} isPost={true} />
                </li>
              </ul>
            </div>
            <div className="panel-footer">
              <CommentCreator currentAuthor={this.props.currentAuthor} post={post} />
            </div>
          </div>
        );
      }
    } else {
      posts = <h3 className="text-center">No posts to see!</h3>;
    }

    return (
      <div className="content-viewer well">
        {posts}
      </div>
    );
  }
});
