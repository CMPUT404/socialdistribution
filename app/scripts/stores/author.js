import _ from 'lodash';
import Reflux from 'reflux';
import Request from '../utils/request';

import Author from '../objects/author';
import AuthorActions from '../actions/author';

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  init: function() {
    // isEmpty calls on ES6 or prototype classes will return true
    // Hence, this must be null when no user is active
    this.currentAuthor = null;
    this.authorList = [];

    this.getAuthors();

    this.listenTo(AuthorActions.login, 'onLogin');
    this.listenTo(AuthorActions.logout, 'logOut');
    this.listenTo(AuthorActions.register, 'onRegister');
    this.listenTo(AuthorActions.checkAuth, 'onCheckAuth');
    this.listenTo(AuthorActions.fetchDetails, 'onFetchDetails');

    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
    this.listenTo(AuthorActions.getAuthorAndListen, this.getAuthorViewData);
    this.listenTo(AuthorActions.subscribeTo, this.subscribeTo);
    this.listenTo(AuthorActions.unsubscribeFrom, this.unsubscribeFrom);

    // Ajax fail listeners
    this.listenTo(AuthorActions.login.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.register.fail, this.ajaxFailed);
    this.listenTo(AuthorActions.fetchDetails.fail, this.ajaxFailed);
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

  // TODO: ajax this
  getAuthors: function () {

  },

  // call this to cache an author in the author list. Also handles updating
  // updating the subscriptionStore
  addAuthorToList: function (authorData) {
    this.authorList.push(new Author(authorData));
  },

  // gets a list of all authors from the server for search purposes
  // TODO: ajax this
  getAuthorNameList: function () {
    var authors = this.authorList.map(function(author) {
      return author.name;
    });
    this.trigger({authorNameList: authors});
  },

  getAuthorIdByName: function (name) {
    for (let author of this.authorList) {
      if (author.name == name) {
        return author.id;
      }
    }
    return null;
  },

  getAuthorById: function (id) {
    for (let author of this.authorList) {
      if (author.isAuthor(id)) {
        return author;
      }
    }
    return undefined;
  },

  getAuthorViewData: function (authorId) {
    for (let author of this.authorList) {
      if (author.id == authorId) {
        this.trigger({displayAuthor: author});
        return;
      }
    }
  },

  // Fires authentication AJAX
  onLogin: function(username, password) {
    Request
      .get('http://localhost:8000/author/login/') //TODO: remove host
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
      .post('http://localhost:8000/author/registration/') //TODO: remove host
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
      this.fetchComplete(this.currentAuthor);
    } else {
      Request
        .get('http://localhost:8000/author/' + id + '/') //TODO: remove host
        .token(this.getToken())
        .promise(this.fetchComplete, AuthorActions.fetchDetails.fail);
    }
  },

  fetchComplete: function(author) {
    this.trigger({displayAuthor: author});
    AuthorActions.fetchDetails.complete(author);
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
