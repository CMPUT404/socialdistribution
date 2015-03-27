import _ from 'lodash';
import Reflux from 'reflux';

import { Request, apiPrefix } from '../utils/request';

import Post from '../objects/post';
import Author from '../objects/author';
import Comment from '../objects/comment';
import AuthorActions from '../actions/author';


// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  init: function() {
    this.currentAuthor = null;
    this.displayAuthor = null;

    this.listenTo(AuthorActions.login,          'onLogin');
    this.listenTo(AuthorActions.logout,         'logOut');
    this.listenTo(AuthorActions.register,       'onRegister');
    this.listenTo(AuthorActions.checkAuth,      'onCheckAuth');
    this.listenTo(AuthorActions.addFriend,      'onAddFriend');
    this.listenTo(AuthorActions.createPost,     'onCreatePost');
    this.listenTo(AuthorActions.deletePost,     'onDeletePost');
    this.listenTo(AuthorActions.fetchAuthor,    'onFetchAuthor');
    this.listenTo(AuthorActions.followFriend,   'onFollowFriend');
    this.listenTo(AuthorActions.unfollowFriend, 'onUnfollowFriend');
    this.listenTo(AuthorActions.createComment,  'onCreateComment');

    // Ajax fail listeners
    this.listenTo(AuthorActions.login.fail,           'ajaxFailed');
    this.listenTo(AuthorActions.register.fail,        'ajaxFailed');
    this.listenTo(AuthorActions.createPost.fail,      'ajaxFailed');
    this.listenTo(AuthorActions.deletePost.fail,      'ajaxFailed');
    this.listenTo(AuthorActions.fetchAuthor.fail,     'ajaxFailed');
    this.listenTo(AuthorActions.addFriend.fail,       'ajaxFailed');
    this.listenTo(AuthorActions.followFriend.fail,    'ajaxFailed');
    this.listenTo(AuthorActions.unfollowFriend.fail,  'ajaxFailed');
    this.listenTo(AuthorActions.createComment.fail,   'ajaxFailed');
  },

  // if in a static method and need acces to store state
  // use the next two methods
  isLoggedIn: function() {
    return !_.isNull(this.currentAuthor);
  },

  getAuthor: function() {
    return this.currentAuthor;
  },

  getToken: function() {
    var token = null;

    if (this.isLoggedIn()) {
        return this.currentAuthor.token;
    }

    return token;
  },

  // Fires authentication AJAX
  onLogin: function(username, password) {
    Request
      .get('/author/login/')
      .use(apiPrefix)
      .auth(username, password)
      .promise(this.loginComplete, AuthorActions.login.fail);
  },

  // Create and save logged in user
  loginComplete: function(authorData) {

    //TODO: store auth token in localStorage

    this.currentAuthor = new Author(authorData.author, authorData.token);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.login.complete(this.currentAuthor);
  },

  // Fires registration AJAX
  onRegister: function(payload) {
    Request
      .post('/author/registration/')
      .use(apiPrefix)
      .send(payload)
      .promise(this.registrationComplete, AuthorActions.register.fail);
  },

  registrationComplete: function(authorData) {
    alertify.success("Registration successful, please wait for an admin's approval");
    AuthorActions.register.complete();
  },

  // check that our author is still logged in, update state of components
  // On page refreshes
  onCheckAuth: function() {

    // TODO: check localStorage here

    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.checkAuth.complete(this.currentAuthor);
  },

  // Fetches author details via AJAX
  onFetchAuthor: function(id, host) {
    Request
      .get('/author/' + id)
      .token(this.getToken())
      .use(apiPrefix)
      .host(host)
      .promise(this.fetchAuthorComplete, AuthorActions.fetchAuthor.fail);
  },

  fetchAuthorComplete: function(authorData) {
    if (this.isLoggedIn() && this.currentAuthor.id === authorData.id) {
      // Update logged-in user's profile
      this.currentAuthor = new Author(authorData, this.currentAuthor.token);
      this.displayAuthor = this.currentAuthor;
    } else {
      this.displayAuthor = new Author(authorData, null);
    }

    this.displayAuthor.posts = this.displayAuthor.posts.map((post) => {
        post = new Post(post);

        if (post.author.id === this.displayAuthor.id) {
          post.author = this.displayAuthor;
        }

        post.comments = post.comments.map((comment) => {
          if (comment.author.id === this.displayAuthor.id) {
            comment.author = this.displayAuthor;
          }

          return comment;
        });

        return post;
    });

    this.trigger({displayAuthor: this.displayAuthor});
    AuthorActions.fetchAuthor.complete(this.displayAuthor);

    if (this.displayAuthor.github_username) {
      Request
        .get('https://api.github.com/users/' + this.displayAuthor.github_username + '/events')
        .promise((result) => {
          this.trigger({gitHubStream: result});
        }, (error) => {
          this.trigger({gitHubStream: []});
          this.ajaxFailed('GitHub: ' + error);
      });
    }
  },

  onCreatePost: function(post) {
    Request
      .post('/post')
      .use(apiPrefix)
      .token(this.getToken())
      .send(post)
      .promise(this.createPostComplete, AuthorActions.createPost.fail);
  },

  createPostComplete: function(postData) {
    var post = new Post(postData);

    // Cyclic reference
    post.author = this.currentAuthor;
    // add new post
    this.currentAuthor.posts.push(post);
    // trigger update
    this.trigger({displayAuthor: this.displayAuthor});
    // this is meant for other stores that are listening
    AuthorActions.createPost.complete(post);
  },

  onDeletePost: function(post) {
    Request
      .del('/post/' + post.guid)
      .use(apiPrefix)
      .token(this.getToken())
      .promise(this.deletePostComplete.bind(this, post),
                AuthorActions.deletePost.fail);
  },

  deletePostComplete: function(post) {
    _.pull(this.currentAuthor.posts, post);

    // trigger update
    this.trigger({displayAuthor: this.displayAuthor});
    // this is meant for other stores that are listening
    AuthorActions.deletePost.complete(post);
  },

  onCreateComment: function(post, comment) {
    Request
      .post('/post/' + post.guid +'/comments')
      .use(apiPrefix)
      .token(this.getToken())
      .send(comment)
      .promise(this.createCommentComplete.bind(this, post),
              AuthorActions.createComment.fail);
  },

  createCommentComplete: function(post, commentData) {
    var comment = new Comment(commentData);

    comment.author = this.currentAuthor;
    post.addComment(comment);

    this.trigger({displayAuthor: this.displayAuthor});
    AuthorActions.createComment.complete(comment);
  },

  onAddFriend: function(request) {
    Request
      .post('/friendrequest')
      .use(apiPrefix)
      .token(this.getToken())
      .send(request)
      .promise(this.addFriendComplete.bind(this, request),
                AuthorActions.addFriend.fail);
  },

  addFriendComplete: function(request) {
    this.currentAuthor.following.push(request.friend.id);
    this.currentAuthor.pending.push(request.friend.id);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.addFriend.complete(request.friend);
  },

  onFollowFriend: function(id) {
    Request
      .get('/author/' + this.currentAuthor.id + '/follow/' + id)
      .use(apiPrefix)
      .token(this.getToken())
      .promise(this.followFriendComplete.bind(this, id),
                AuthorActions.followFriend.fail);
  },

  followFriendComplete: function(id) {
    this.currentAuthor.following.push(id);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.followFriend.complete(id);
  },

  onUnfollowFriend: function(id) {
    Request
      .del('/author/' + this.currentAuthor.id + '/follow/' + id)
      .use(apiPrefix)
      .token(this.getToken())
      .promise(this.unfollowFriendComplete.bind(this, id),
                AuthorActions.unfollowFriend.fail);
  },

  unfollowFriendComplete: function(id) {
    _.pull(this.currentAuthor.friends, id);
    _.pull(this.currentAuthor.following, id);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.followFriend.complete(id);
  },
  // This is a listener not a handler
  // `logOut` doesn't require any AJAX calls
  logOut: function() {
    this.currentAuthor = null;
    this.trigger({currentAuthor: this.currentAuthor});
  },

  // Catches all failed requests via actions listeners
  ajaxFailed: function(error) {
    alertify.error(error);
  },

});
