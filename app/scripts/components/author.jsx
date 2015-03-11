import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { State } from 'react-router';
import { Col } from 'react-bootstrap';

import PostStore from '../stores/post';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';
import ContentViewer from './contentviewer';
import ContentCreator from './contentcreator';
import Follow from './follow';
import Spinner from './spinner';

// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), Reflux.connect(PostStore), State],

  // statics: {
  //
  //   // since the author component can sometimes be mounted in the background,
  //   // ensure we update the author if we're not coming back to the same one
  //   willTransitionTo: function (transition, params) {
  //     AuthorActions.getAuthorAndListen(params.id);
  //   },
  //
  //   willTransitionFrom: function () {
  //     AuthorActions.unbindAuthorListener();
  //   }
  // },

  getInitialState: function() {
    return {
      displayAuthor: null,
      authorPosts: [],
    };
  },

  componentDidMount: function () {
    AuthorActions.fetchDetails(this.getParams().id);
  },

  render: function() {
    // if we haven't gotten our initial data yet, put a spinner in place
    if (_.isNull(this.state.displayAuthor) || _.isNull(this.state.authorPosts)) {
      return (<Spinner />);
    }

    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorViewId = this.getParams().id;
    var contentCreator, follow;

    // see if the viewer is logged in
    if (!_.isNull(this.props.currentAuthor)) {

      // if viewing their own profile
      if (this.props.currentAuthor.isAuthor(authorViewId)) {
        contentCreator = <ContentCreator currentAuthor={this.props.currentAuthor} />;
      } else {
        follow = <Follow currentAuthor={this.props.currentAuthor} author={this.state.displayAuthor} />;
      }
    }

    return (
      <Col md={12}>
        <div className="media well author-biography">
          <div className="media-left">
            <img className="media-object profile-image" src={this.state.displayAuthor.getImage()} />
          </div>
          <div className="media-body">
            <h4 className="media-heading">{this.state.displayAuthor.displayname}</h4>
            <h2 className="media-heading">{this.state.displayAuthor.getName()}</h2>
            <p><strong>Bio:</strong> {this.state.displayAuthor.bio}</p>
            <p><strong>Email:</strong> {this.state.displayAuthor.email}</p>
            {/**<p><strong>Following:</strong> {this.state.displayAuthor.getSubscriptionCount()}</p>*/}
            {/**<p><strong>Followers:</strong> {this.state.displayAuthor.getSubscriberCount()}</p>**/}
            <p><a href={this.state.displayAuthor.getGithub()} target="_blank">Github</a></p>
            {follow}
          </div>
        </div>
        <div className="jumbotron">
        {contentCreator}
        </div>
        <ContentViewer
          currentAuthor={this.props.currentAuthor}
          posts={this.state.authorPosts} />
      </Col>
    );
  }
});
