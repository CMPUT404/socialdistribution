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
import Follow from './follow';

// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

mixins: [Reflux.connect(AuthorStore), Reflux.connect(PostStore), State],

  statics: {

    // since the author component can sometimes be mounted in the background,
    // ensure we update the author if we're not coming back to the same one
    willTransitionTo: function (transition, params) {
      AuthorActions.getAuthorAndListen(params.id);
    },

    willTransitionFrom: function () {
      AuthorActions.unbindAuthorListener();
    }
  },

  getInitialState: function() {
    return {
      displayAuthor: {},
      authorPosts: []
    };
  },

  componentDidMount: function () {
    AuthorActions.getAuthorAndListen(this.getParams().id);
  },

  render: function() {

    // if we haven't gotten our initial data yet, put a spinner in place
    if (Check.emptyObject(this.state.displayAuthor)) {
      return (<i className="fa fa-refresh fa-spin fa-5x"></i>);
    }

    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var authorViewId = this.getParams().id;
    var contentCreator, follow;

    // see if the viewer is logged in
    if (!Check.emptyObject(this.props.currentAuthor)) {

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
            <h4 className="media-heading">{this.state.displayAuthor.name}</h4>
            <p><strong>Bio:</strong> {this.state.displayAuthor.bio}</p>
            <p><strong>Following:</strong> {this.state.displayAuthor.getSubscriptionCount()}</p>
            <p><strong>Followers:</strong> {this.state.displayAuthor.getSubscriberCount()}</p>
            <p><a href={this.state.displayAuthor.github} target="_blank">Github</a></p>
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
