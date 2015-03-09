import Reflux from 'reflux';
import UUID from 'uuid';
import AuthorActions from '../actions/author';

var FIXTURE = {
  name: "Bert McGert",
  id: 1234,
  author_image: "images/bert.jpg",
  friend_request_count: 3,
  notifications: {}
};

var ALIST = [
{
  id: "4567",
  name: "Benny Bennassi",
  image: "images/benny.jpg"
},
{
  id: "9876",
  name: "Kanye West",
  image: "images/kanye.jpg",
},
{
  id: "2192",
  name: "David Guetta",
  image: "images/david.jpg",
}];

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  currentAuthor: FIXTURE,

  authorList: ALIST,

  init: function() {
    this.listenTo(AuthorActions.login.completed, this.loginCompleted);
    this.listenTo(AuthorActions.login.failed, this.loginFailed);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
  },

  // gets a list of all authors from the server for search purposes
  // TODO: ajax this
  getAuthorNameList: function () {
    return this.trigger({authorList: this.authorList.map(function(author) {
      return author.name;
    })});
  },

  getAuthorIdByName: function (name) {
    for (let author of this.authorList) {
      if (author.name == name) {
        return author.id;
      }
    }
    return null;
  },

  getCurrentAuthor: function () {
    return this.currentAuthor;
  },

  // Handles logging the user in using the provided credentials
  // Also need to set our basic auth token somewhere
  loginCompleted: function(author) {
    this.currentAuthor = author;
    this.trigger({"currentAuthor": author});
  },

  loginFailed: function(res) {
    alertify.error("Login failed! " + res.error);
  },

  logOut: function() {
    this.currentAuthor = undefined;
    this.trigger( {"currentAuthor": undefined} );
  }
});
