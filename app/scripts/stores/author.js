import Reflux from 'reflux';
import UUID from 'uuid';
import AuthorActions from '../actions/author';

var ALIST = [{
  name: "Bert McGert",
  id: "1234",
  bio: "I'm a fun loving guy who loves to learn",
  image: "images/bert.jpg",
  friend_request_count: 3,
  notifications: []
},
{
  id: "4567",
  name: "Benny Bennassi",
  image: "images/benny.jpg",
  bio: "I love satisfcation"
},
{
  id: "9876",
  name: "Kanye West",
  image: "images/kanye.jpg",
  bio: "I think I'm the greatest rapper alive"
},
{
  id: "2192",
  name: "David Guetta",
  image: "images/david.jpg",
  bio: "I have an over inflated ego"
}];

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  init: function() {

    this.currentAuthor = {};
    this.authorList = ALIST;

    this.listenTo(AuthorActions.checkAuth, this.checkAuth);
    this.listenTo(AuthorActions.login.completed, this.loginCompleted);
    this.listenTo(AuthorActions.login.failed, this.loginFailed);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
    this.listenTo(AuthorActions.getAuthorViewData, this.getAuthorViewData);
    this.listenTo(AuthorActions.getAuthorAndListen, this.getAuthorViewData);
    this.listenTo(AuthorActions.subscribeTo, this.subscribeTo);
    this.listenTo(AuthorActions.unsubscribeFrom, this.unsubscribeFrom);
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

  // check that our author is still logged in, update state of components
  checkAuth: function () {
    // TODO: ajax get author info rather than simply spoofing a successful auth
    var author = ALIST[1];
    if (author) {
      this.loginCompleted(author);
    }
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

  loginFailed: function(res) {
    alertify.error("Login failed! " + res.error);
  },

  logOut: function() {
    this.currentAuthor = {};
    this.trigger({currentAuthor: this.currentAuthor, loggedOut: true});
  }
});
