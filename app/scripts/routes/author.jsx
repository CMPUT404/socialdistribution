import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { State, Navigation } from 'react-router';

import {
  Button,
  Col,
  Row,
  TabbedArea,
  TabPane,
  ModalTrigger
} from 'react-bootstrap';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

import ContentViewer from '../components/content/content-viewer';
import PostCreator from '../components/content/post-creator';
import ProfileLink from '../components/content/profile-link';
import ProfileModal from '../components/profile-modal';
import ListAuthors from '../components/list-authors';
import Stream from '../components/github/stream';
import Subscribe from '../components/subscribe';
import Spinner from '../components/spinner';


// Represents a prfoile page.
// It should only display a list of posts created by the author
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), Reflux.ListenerMixin, Navigation, State],

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

  formatParams: function(params) {
    if (!_.isUndefined(params.host)) {
      params.host = decodeURIComponent(params.host);
    }

    if (AuthorStore.isLoggedIn() && params.id === 'profile') {
      params.id = AuthorStore.getAuthor().id;
    }

    return params;
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
    var newParams = this.formatParams(this.getParams());

    if (newParams.id !== this.params.id &&
        newParams.host !== this.params.host) {
      this.params = newParams;
      this.refresh(this.params);
    }
  },

  refresh: function(params) {
    AuthorActions.fetchAuthor(params.id, params.host);
  },

  componentDidMount: function () {
    this.listenTo(AuthorActions.logout, () => this.transitionTo('login'));
    this.params = this.formatParams(this.getParams());
    this.refresh(this.params);
  },

  render: function() {
    // if we haven't gotten our initial data yet, put a spinner in place
    if (_.isNull(this.state.displayAuthor)) {
      return (<Spinner />);
    }

    var postCreator, ghStream, githubUrl, editProfile;
    var contentTitle, friendsTitle;

    githubUrl = this.state.displayAuthor.getGithubUrl();

    // see if the viewer is logged in
    // and if viewing their own profile
    if (!_.isNull(this.props.currentAuthor) &&
        this.props.currentAuthor.isAuthor(this.params.id)) {
      postCreator = (
        <div className="jumbotron">
          <PostCreator currentAuthor={this.props.currentAuthor} />
        </div>
      );

      editProfile = (
        <ModalTrigger modal={<ProfileModal />}>
          <i className="fa fa-pencil"></i>
        </ModalTrigger>
      );
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

    contentTitle = <span>Posts <span className="badge">{this.state.displayAuthor.posts.length}</span></span>
    friendsTitle = <span>Friends <span className="badge">{this.state.displayAuthor.friends.length}</span></span>

    return (
      <Row>
        <Col md={8}>
          <div className="media well author-biography">
            <span className="pull-right edit-prifle">
              {editProfile}
            </span>
            <div className="media-left">
              <img className="media-object profile-image" src={this.state.displayAuthor.image} />
            </div>
            <Row className="media-body">
              <Col md={6}>
                <h2 className="media-heading text-capitalize">{this.state.displayAuthor.getName()}</h2>
                <h4 className="media-heading text-capitalize">{this.state.displayAuthor.displayname}</h4>
                <p>{this.state.displayAuthor.bio}</p>
                <p>{this.state.displayAuthor.email}</p>
                {githubUrl}
              </Col>
              <Col md={6}>
                <Subscribe className="pull-right" author={this.state.displayAuthor} />
              </Col>
            </Row>
          </div>
          {postCreator}
          <div className="author-tabs">
            <TabbedArea defaultActiveKey={1}>
              <TabPane eventKey={1} tab={contentTitle}>
                <ContentViewer
                  currentAuthor={this.props.currentAuthor}
                  posts={this.state.displayAuthor.sortedPosts()} />
              </TabPane>
              <TabPane eventKey={2} tab={friendsTitle} className="well">
                <ListAuthors authors={this.state.displayAuthor.friends} />
              </TabPane>
            </TabbedArea>
          </div>
        </Col>
        <Col md={4}>
          {ghStream}
        </Col>
      </Row>
    );
  }
});
