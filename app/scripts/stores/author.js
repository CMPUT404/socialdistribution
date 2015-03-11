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

    this.listenTo(AuthorActions.checkAuth, this.checkAuth);

    // Actions
    this.listenTo(AuthorActions.login, 'onLogin');
    this.listenTo(AuthorActions.register, 'onRegister');
    this.listenTo(AuthorActions.fetchDetails, 'onFetchDetails');

    // Handler declarations
    this.listenTo(AuthorActions.login.completed, this.loginCompleted);
    this.listenTo(AuthorActions.login.failed, this.ajaxFailed);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
    this.listenTo(AuthorActions.getAuthorAndListen, this.getAuthorViewData);
    this.listenTo(AuthorActions.subscribeTo, this.subscribeTo);
    this.listenTo(AuthorActions.unsubscribeFrom, this.unsubscribeFrom);
    this.listenTo(AuthorActions.register.completed, this.registrationComplete);
    this.listenTo(AuthorActions.register.failed, this.ajaxFailed);
    this.listenTo(AuthorActions.fetchDetails.completed, this.fetchComplete);
    this.listenTo(AuthorActions.register.failed, this.ajaxFailed);

  },

  // Action Executioners
  onLogin: function(username, password) {
    Request
      .get('http://localhost:8000/author/login/') //TODO: remove host
      .auth(username, password)
      .promise()
      .then( AuthorActions.login.completed )
      .catch( AuthorActions.login.failed );
  },

  onRegister: function(payload) {
    Request
      .post('http://localhost:8000/author/registration/') //TODO: remove host
      .send(payload)
      .promise()
      .then( AuthorActions.register.completed )
      .catch( AuthorActions.register.failed );
  },

  onFetchDetails: function(id) {
    if (this.isLoggedIn() && id === this.currentAuthor.id) {
      AuthorActions.fetchDetails.completed(this.currentAuthor);
    } else {
      Request
        .get('http://localhost:8000/author/' + id + '/') //TODO: remove host
        .token(this.getToken())
        .promise()
        .then( AuthorActions.fetchDetails.completed )
        .catch( AuthorActions.fetchDetails.failed );
    }
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
        token = this.currentAuthor.token;
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

  // Action Handlers

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

  // check that our author is still logged in, update state of components
  checkAuth: function () {
    this.trigger({currentAuthor: this.currentAuthor});
  },

  logOut: function() {
    this.currentAuthor = null;
    this.trigger({currentAuthor: this.currentAuthor, loggedOut: true});
  },

  // AJAX Handlers //

  // Handles logging the user in using the provided credentials
  // Also need to set our basic auth token somewhere
  loginCompleted: function(authorData) {
    //TODO: store basic auth token in localStorage
    this.currentAuthor = new Author(authorData.author, authorData.token);
    this.trigger({currentAuthor: this.currentAuthor});
  },

  registrationComplete: function(author) {
    this.loginCompleted(author);
  },

  fetchComplete: function(author) {
    this.trigger({displayAuthor: author});
  },

  ajaxFailed: function(error) {
    alertify.error(error);
  },


});
