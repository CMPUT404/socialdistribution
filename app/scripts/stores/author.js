import Reflux from 'reflux';

import Author from '../objects/author';
import AuthorActions from '../actions/author';

var ALIST = [{
  name: "Bert McGert",
  id: "1234",
  bio: "I'm a fun loving guy who loves to learn",
  image: "images/bert.jpg",
  subscriptions: ["4567","9876"],
  friend_request_count: 3,
  notifications: []
},
{
  id: "4567",
  name: "Benny Bennassi",
  image: "images/benny.jpg",
  bio: "I love satisfcation",
  subscriptions: ["1234","9876"],
  friend_request_count: 1,
},
{
  id: "9876",
  name: "Kanye West",
  image: "images/kanye.jpg",
  bio: "I think I'm the greatest rapper alive",
  subscriptions: ["1234"]
},
{
  id: "2192",
  name: "David Guetta",
  image: "images/david.jpg",
  bio: "I have an over inflated ego",
  subscriptions: ["4567","9876"],
}];

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  init: function() {

    this.currentAuthor = {};
    this.authorList = [];
    this.subscriptionStore = new Map();

    this.getAuthors();

    this.listenTo(AuthorActions.checkAuth, this.checkAuth);
    this.listenTo(AuthorActions.login.completed, this.loginCompleted);
    this.listenTo(AuthorActions.login.failed, this.ajaxFailed);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
    this.listenTo(AuthorActions.getAuthorAndListen, this.getAuthorViewData);
    this.listenTo(AuthorActions.subscribeTo, this.subscribeTo);
    this.listenTo(AuthorActions.unsubscribeFrom, this.unsubscribeFrom);
    this.listenTo(AuthorActions.register.completed, this.registrationComplete);
    this.listenTo(AuthorActions.register.failed, this.ajaxFailed);
  },

  // TODO: ajax this
  getAuthors: function () {
    var authorListData = ALIST;
    for (let author of authorListData) {
      this.addAuthorToList(author);
    }
  },

  // call this to cache an author in the author list. Also handles updating
  // updating the subscriptionStore
  addAuthorToList: function (authorData) {
    this.authorList.push(new Author(authorData, this.subscriptionStore));
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
    // TODO: ajax get author info rather than simply spoofing a successful auth
    var author = this.authorList[0];
    if (author) {
      this.loginCompleted(author);
    }
  },

  // Handles logging the user in using the provided credentials
  // Also need to set our basic auth token somewhere
  loginCompleted: function(author) {
    //TODO: store basic auth token in localStorage
    this.currentAuthor = author;
    this.trigger({currentAuthor: this.currentAuthor});
  },

  registrationComplete: function(author) {
    this.loginCompleted(author);
  },

  ajaxFailed: function(error) {
    alertify.error(error);
  },

  logOut: function() {
    this.currentAuthor = {};
    this.trigger({currentAuthor: this.currentAuthor, loggedOut: true});
  }
});
