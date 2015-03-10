import _ from 'lodash';
import React from 'react';

import ContentCreator from './contentcreator';
import Content from './content';

// This is used to bundle up user content we wish to display. Namely posts and
// comments. It listens to and updates based on changes in the Post Store.
export default React.createClass({

  render: function() {
    var posts = [];

    if (_.isUndefined(this.props.posts)) {
      return (<i className="fa fa-refresh fa-spin fa-5x"></i>);
    }

    // orders posts if any are passed in as props
    if (this.props.posts.length > 0) {
      for (let post of this.props.posts) {
        posts.push(
          <div className="panel panel-default" key={"post-"+post.id}>
            <div className="panel-body">
              <ul className="media-list">
                <li className="media">
                  <Content data={post} isPost={true} />
                </li>
              </ul>
            </div>
            <div className="panel-footer">
              <ContentCreator key={"comment-creator-" + post.id} currentAuthor={this.props.currentAuthor} post={post} forComment={true} />
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
