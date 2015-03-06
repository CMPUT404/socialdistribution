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

var AUTHORLIST = [{
  id: "4567",
  name: "Benny Bennassi",
  image: "images/benny.jpg"
}, {
  id: "9876",
  name: "Kanye West",
  image: "images/kanye.jpg",
}, {
  id: "2192",
  name: "David Guetta",
  image: "images/david.jpg",
}];

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
export default Reflux.createStore({

  currentAuthor: FIXTURE,

  authorList: AUTHORLIST,

  init: function() {
    this.listenTo(AuthorActions.login, this.logIn);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorList, this.getAuthorList);
  },

  // gets a list of all authors from the server for search purposes
  // TODO: ajax this
  getAuthorList: function () {
    return this.trigger({"authorList": this.authorList});
  },

  getCurrentAuthor: function () {
    return this.currentAuthor;
  },

  // Handles logging the user in using the provided credentials
  // Also need to set our basic auth token somewhere
  logIn: function() {

  },

  logOut: function() {
    this.currentAuthor = undefined;
    this.trigger( {"currentAuthor": undefined} );
  }
});
