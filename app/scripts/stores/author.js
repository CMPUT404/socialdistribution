var Reflux = require('reflux');
var UUID = require('uuid');
var AuthorActions = require('../actions/author');


var FIXTURE = {
  name: "Bert McGert",
  id: 1234,
  author_image: "images/bert.jpg",
  friend_request_count: 3
};

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
var AuthorStore = Reflux.createStore({

    currentAuthor: FIXTURE,

    init: function() {
      this.listenTo(AuthorActions.login, this.logIn);
      this.listenTo(AuthorActions.logout, this.logOut);
    },

    getCurrentAuthor: function () {
        return this.currentAuthor;
    },

    logIn: function() {

    },
    logOut: function() {
      this.currentAuthor = undefined;
      this.trigger( {"currentAuthor": undefined} );
    }
});

module.exports = AuthorStore;
