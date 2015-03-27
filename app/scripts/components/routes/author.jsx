import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { State, Navigation } from 'react-router';
import { Col, Row, Button } from 'react-bootstrap';

import AuthorStore from '../../stores/author';
import AuthorActions from '../../actions/author';
import Follow from '../subscribe';
import Spinner from '../spinner';
import Stream from '../github/stream';

import ContentViewer from '../content/content-viewer';
import PostCreator from '../content/post-creator';

import ActionListener from '../../mixins/action-listener';

// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), ActionListener, Navigation, State],

  statics: {
    willTransitionTo: function(transition, params) {
      if (params.id === 'profile' && !AuthorStore.isLoggedIn()) {
        transition.redirect('login')
      }
    }
  },

  getInitialState: function() {
    return {
      displayAuthor: null,
      gitHubStream: null
    };
  },

  onLogout: function() {
    this.transitionTo('login');
  },

  updateParams: function() {
    this.params = this.getParams();

    if (!_.isUndefined(this.params.host)) {
      this.params.host = decodeURIComponent(this.params.host);
    }

    if (this.params.id === 'profile') {
      this.params.id = AuthorStore.getAuthor().id;
    }
  },

  // https://github.com/rackt/react-router/blob/master/docs/guides/overview.md#important-note-about-dynamic-segments
  componentWillReceiveProps: function(nextProps) {
    if (_.isNull(nextProps.currentAuthor)) {
      this.onLogout();
    } else {
      this.updateParams();
      this.refresh();
    }
  },

  refresh: function() {
    AuthorActions.fetchAuthor(this.params.id, this.params.host);
  },

  componentDidMount: function () {
    this.listen(AuthorActions.logout, this.onLogout);
    this.updateParams();
    this.refresh();
  },

  render: function() {
    // if we haven't gotten our initial data yet, put a spinner in place
    if (_.isNull(this.state.displayAuthor)) {
      return (<Spinner />);
    }

    // this comes from the RouterState mixin and lets us pull an author id out
    // of the uri so we can fetch their posts.
    var postCreator, follow, ghStream, githubUrl;

    githubUrl = this.state.displayAuthor.getGithubUrl();

    // see if the viewer is logged in
    if (!_.isNull(this.props.currentAuthor)) {

      // if viewing their own profile
      if (this.props.currentAuthor.isAuthor(this.params.id)) {
        postCreator = <div className="jumbotron"><PostCreator currentAuthor={this.props.currentAuthor} /></div>;
      } else {
        follow = <Follow className="pull-right" author={this.state.displayAuthor} />;
      }
    }

    if (!_.isNull(githubUrl)) {
      githubUrl = <p><a href={githubUrl} target="_blank">Github</a></p>;

      if (_.isNull(this.state.gitHubStream)) {
        ghStream = <Spinner />;
      } else {
        ghStream = (
          <Row>
            <h3>GitHub Stream</h3>
            <Stream events={this.state.gitHubStream} />
          </Row>
        );
      }
    }

    return (
      <Row>
        <Col md={8}>
          <div className="media well author-biography">
            <div className="media-left">
              <img className="media-object profile-image" src={this.state.displayAuthor.getImage()} />
            </div>
            <div className="media-body">
              <Col md={6}>
                <h2 className="media-heading">{this.state.displayAuthor.getName()}</h2>
                <h4 className="media-heading">{this.state.displayAuthor.displayname}</h4>
                <p>{this.state.displayAuthor.bio}</p>
                <p>{this.state.displayAuthor.email}</p>
                {githubUrl}
              </Col>
              <Col md={6}>
                {follow}
              </Col>
            </div>
          </div>
          {postCreator}
          <ul className="nav nav-tabs author-tabs">
            <li role="presentation" className="active">
              <a href="#posts-tab" aria-controls="posts-tab" role="tab" data-toggle="tab">Posts <span className="badge">{this.state.displayAuthor.posts.length}</span></a>
            </li>
            <li role="presentation" className="">
              <a href="#friends-tab" aria-controls="preview-tab" role="tab" data-toggle="tab">Friends <span className="badge">{this.state.displayAuthor.friends.length}</span></a>
            </li>
          </ul>
          <div className="tab-content">
            <div role="tabpanel" className="tab-pane active" id="posts-tab">
              <ContentViewer
                currentAuthor={this.props.currentAuthor}
                posts={this.state.displayAuthor.sortedPosts()} />
            </div>
            <div role="tabpanel" className="tab-pane active" id="friends-tab">
            </div>
          </div>
        </Col>
        <Col md={4}>
          {ghStream}
        </Col>
      </Row>
    );
  }
});
