import _ from 'lodash';
import Reflux from 'reflux';

import Request from '../utils/request';

import Post from '../objects/post';
import Author from '../objects/author';
import Comment from '../objects/comment';
import AuthorActions from '../actions/author';

import { responseToPosts } from './post';

// TODO:
// * In prod, remove host API prefixes in AJAX calls
var __API__ = 'http://localhost:8000';

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  init: function() {
    this.currentAuthor = null;
    this.displayAuthor = null;

    this.listenTo(AuthorActions.login, 'onLogin');
    this.listenTo(AuthorActions.logout, 'logOut');
    this.listenTo(AuthorActions.register, 'onRegister');
    this.listenTo(AuthorActions.checkAuth, 'onCheckAuth');
    this.listenTo(AuthorActions.addFriend, 'onAddFriend');
    this.listenTo(AuthorActions.createPost, 'onCreatePost');
    this.listenTo(AuthorActions.fetchPosts, 'onFetchPosts');
    this.listenTo(AuthorActions.followFriend,'onFollowFriend');
    this.listenTo(AuthorActions.fetchDetails, 'onFetchDetails');
    this.listenTo(AuthorActions.createComment, 'onCreateComment');

    // Ajax fail listeners
    this.listenTo(AuthorActions.login.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.register.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.createPost.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.fetchPosts.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.fetchDetails.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.followFriend.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.createComment.fail, this.ajaxFailed);
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
      .get(__API__ + '/author/login/') //TODO: remove host
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
      .post(__API__ + '/author/registration/') //TODO: remove host
      .send(payload)
      .promise(this.registrationComplete, AuthorActions.register.fail);
  },

  // Treat post-registration as a login
  registrationComplete: function(authorData) {
    this.loginComplete(authorData);
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
  onFetchDetails: function(id) {
    // If logged-in user wants to see their own profile
    // no need to AJAX, we already have that info from login/register
    if (this.isLoggedIn() && id === this.currentAuthor.id) {
      this.displayAuthor = this.currentAuthor;
      this.trigger({displayAuthor: this.displayAuthor});
      AuthorActions.fetchDetails.complete(this.displayAuthorhor);
      this.fetchGHStream();
    } else {
      Request
        .get(__API__ + '/author/' + id) //TODO: remove host
        .promise(this.fetchDetailsComplete, AuthorActions.fetchDetails.fail);
    }
  },

  fetchDetailsComplete: function(authorData) {
    this.displayAuthor = new Author(authorData, null);
    this.trigger({displayAuthor: this.displayAuthor});
    AuthorActions.fetchDetails.complete(this.displayAuthor);
    this.fetchGHStream();
  },

  fetchGHStream: function() {
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

  // Fetches author's posts
  onFetchPosts: function(id) {
    Request
      .get(__API__ + '/author/' + id + '/posts') //TODO: remove host
      .token(this.getToken())
      .promise(this.fetchPostsComplete.bind(this, id), AuthorActions.fetchPosts.fail);
  },

  fetchPostsComplete: function(id, postsData) {
    var posts = responseToPosts(postsData);

    posts.forEach((post) => {
      post.author = this.displayAuthor;

      post.comments.forEach((comment) => {
        if (comment.author.id == this.displayAuthor.id) {
          comment.author = this.displayAuthor;
        } else {
          comment.author = new Author(comment.author);
        }
      });
    });

    this.displayAuthor.posts = posts;
    this.trigger({displayAuthor: this.displayAuthor});
  },

  onCreatePost: function(post) {
    Request
      .post(__API__ + '/post')
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

  onCreateComment: function(post, comment) {
    Request
      .post(__API__ + '/post/' + post.guid +'/comments')
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

  // WIP..

  subscribeTo: function (author) {
    // find authors and add subscriber
    this.currentAuthor.subscribeTo(author);
    // TODO: ajax call here to persist
  },

  // unsubscribes the current user from the specified author
  unsubscribeFrom: function (author) {
    // find authors and add subscriber
    this.currentAuthor.unsubscribeFrom(author);
    // TODO: ajax call here to persist
  },

});
