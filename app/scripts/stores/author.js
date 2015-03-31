import _ from 'lodash';
import Reflux from 'reflux';

import { Request, apiPrefix } from '../utils/helpers';

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
    this.authorsList   = [];

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
    this.listenTo(AuthorActions.getAuthors,     'onGetAuthors');
    this.listenTo(AuthorActions.update,         'onUpdate');

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
    this.listenTo(AuthorActions.update.fail,          'ajaxFailed');
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
  onLogin: function(username, password, token = null) {
    Request
      .get('/author/login/')
      .use(apiPrefix)
      .token(token)
      .basic(username, password)
      .promise(this.loginComplete, AuthorActions.login.fail);
  },

  // Create and save logged in user
  loginComplete: function(authorData) {
    sessionStorage.setItem('token', authorData.token);
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
    var token = sessionStorage.getItem('token');

    if (!_.isNull(token)) {
      this.onLogin(null, null, token);
    }
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
      this.displayAuthor = new Author(authorData);
    }

    // async
    this.fetchGithubStream();

    this.displayAuthor.posts = authorData.posts.map((post) => {
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
  },

  fetchGithubStream: function() {
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

  onAddFriend: function(friend) {
    // Manual construction is needed for two reasons
    // 1. Privacy (currentAuthor has stuff we don't want to send)
    // 2. Crazy circular references that break JSON.stringify
    let request = {
      query: "friendrequest",
      author: {
        id         : this.currentAuthor.id,
        url        : this.currentAuthor.url,
        host       : this.currentAuthor.host,
        displayname: this.currentAuthor.displayname
      },
      friend: {
        id         : friend.id,
        url        : friend.url,
        host       : friend.host,
        displayname: friend.displayname
      }
    };

    Request
      .post('/friendrequest')
      .use(apiPrefix)
      .token(this.getToken())
      .send(request)
      .promise(this.addFriendComplete.bind(this, request.friend),
                AuthorActions.addFriend.fail);
  },

  addFriendComplete: function(friend) {
    this.currentAuthor.following.push(friend);

    if (this.currentAuthor.inList('requests', friend)) {
      this.currentAuthor.removeFrom('requests', friend);
      this.currentAuthor.addTo('friends', friend);
    } else {
      this.currentAuthor.addTo('pending', friend);
    }

    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.addFriend.complete(friend);
  },

  onFollowFriend: function(friend) {
    let request = {
      author: {
        id         : this.currentAuthor.id,
        url        : this.currentAuthor.url,
        host       : this.currentAuthor.host,
        displayname: this.currentAuthor.displayname
      },
      following: {
        id         : friend.id,
        url        : friend.url,
        host       : friend.host,
        displayname: friend.displayname
      }
    };

    Request
      .post('/author/' + this.currentAuthor.id + '/follow')
      .use(apiPrefix)
      .token(this.getToken())
      .send(request)
      .promise(this.followFriendComplete.bind(this, friend),
                AuthorActions.followFriend.fail);
  },

  followFriendComplete: function(friend) {
    this.currentAuthor.following.push(friend);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.followFriend.complete(friend);
  },

  onUnfollowFriend: function(friend) {
    Request
      .del('/author/' + this.currentAuthor.id + '/follow/' + friend.id)
      .use(apiPrefix)
      .token(this.getToken())
      .promise(this.unfollowFriendComplete.bind(this, friend),
                AuthorActions.unfollowFriend.fail);
  },

  unfollowFriendComplete: function(friend) {
    this.currentAuthor.removeFrom('friends', friend);
    this.currentAuthor.removeFrom('pending', friend);
    this.currentAuthor.removeFrom('following', friend);
    this.trigger({currentAuthor: this.currentAuthor});
    AuthorActions.followFriend.complete(friend);
  },

  onGetAuthors: function() {
    Request
      .get('/authors')
      .use(apiPrefix)
      .promise(this.getAuthorsComplete, AuthorActions.getAuthors.fail);
  },

  getAuthorsComplete: function(result) {
    this.authorsList = result.authors.filter((authorData) => {
      if (this.isLoggedIn()) {
        return authorData.id !== this.getAuthor().id;
      }
      return true;
    }).map(authorData => new Author(authorData));

    this.trigger({authorsList: this.authorsList});
    AuthorActions.getAuthors.complete(this.authorsList);
  },

  onUpdate: function(data) {
    Request
      .post('/author/profile')
      .use(apiPrefix)
      .token(this.getToken())
      .send(data)
      .promise(this.updateComplete, AuthorActions.update.fail);
  },

  updateComplete: function(authorData) {
    var newAuthor = new Author(authorData, this.currentAuthor.token);
    newAuthor.post = this.currentAuthor.posts;
    //updates can only occur from /author route
    this.displayAuthor = newAuthor;
    this.currentAuthor = newAuthor;

    this.fetchGithubStream();

    this.trigger({
      currentAuthor: this.currentAuthor,
      displayAuthor: this.displayAuthor
    });

    AuthorActions.update.complete(this.currentAuthor);
  },

  // This is a listener not a handler
  // fire it but don't worry about the response
  // this should never fail
  logOut: function() {
    Request
      .del('/author/login/')
      .use(apiPrefix)
      .token(this.getToken())
      .end()

    sessionStorage.clear();
    this.currentAuthor = null;
    this.trigger({currentAuthor: this.currentAuthor});
  },

  // Catches all failed requests via actions listeners
  ajaxFailed: function(error) {
    alertify.error(error);
  },

});
