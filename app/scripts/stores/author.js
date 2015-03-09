import Reflux from 'reflux';
import UUID from 'uuid';
import AuthorActions from '../actions/author';

var FIXTURE = {
  name: "Bert McGert",
  id: 1234,
  bio: "I'm a fun loving guy who loves to learn",
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
    this.listenTo(AuthorActions.refreshAuthor, this.refreshAuthor);
    this.listenTo(AuthorActions.login, this.logIn);
    this.listenTo(AuthorActions.logout, this.logOut);
    this.listenTo(AuthorActions.getAuthorNameList, this.getAuthorNameList);
  },

  // gets a list of all authors from the server for search purposes
  // TODO: ajax this
  getAuthorNameList: function () {
    this.trigger({authorList: this.authorList.map(function(author) {
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

  // check that our author is still logged in, update state of components
  refreshAuthor: function () {
    this.trigger({currentAuthor: this.currentAuthor});
  },

  // Handles logging the user in using the provided credentials
  // Also need to set our basic auth token somewhere
  logIn: function() {

  },

  logOut: function() {
    this.currentAuthor = undefined;
    this.trigger({currentAuthor: undefined});
  }
});
