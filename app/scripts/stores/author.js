var Reflux = require('reflux');
var UUID = require('uuid');

// Deals with store Author information. Both for the logged in user and other
// author's we need to load with their content.
var AuthorStore = Reflux.createStore({

    current_author: "1234",

    authors: new Map(),

    init: function() {

        this.author = this.getAuthors();

        // fetches the list of most recent posts
        // this.listenTo(PostActions.newPost, this.addPost);
    },

    getAuthors: function () {
        var author = {
          name: "Bert McGert",
          id: this.current_author,
          author_image: "images/bert.jpg",
          friend_request_count: 3
        };
        this.authors.set(author.id, author);
    },

    getCurrentAuthor: function () {
        return this.authors.get(this.current_author);
    },

    getCurrentAuthorId: function () {
        return this.getCurrentAuthor().id;
    }
});

module.exports = AuthorStore;
