var Reflux = require('reflux');
var UUID = require('uuid');
var PostActions = require('../actions/post');

// Deals with App State Machine state
var PostStore = Reflux.createStore({

    init: function() {
        // fetches the list of most recent posts
        this.posts = this.getPosts();

        // Listeners
        this.listenTo(PostActions.newPost, this.newPost);
        this.listenTo(PostActions.newComment, this.newComment);
        this.listenTo(PostActions.refreshPosts, this.refreshPosts);
    },

    // Handles fetching posts based on query.
    getPosts: function (query) {
        // TODO: AJAX and remove defaultPost placeholder
        return this.defaultPosts();
    },

    refreshPosts: function (query) {
        //TODO: ajax
        this.trigger({"posts": this.posts});
    },

    // Used to mock data out
    defaultPosts: function (query) {

        var map = new Map();
        var uuid = UUID.v4();

        map.set(uuid, {
            id: uuid,
            author_id: "4567",
            author_name: "Benny Bennassi",
            author_image: "images/benny.jpg",
            content: "Check out my new hit satisfaction",
            type: "raw",
            timestamp: "1423952298",
            comments: [{
                id: UUID.v4(),
                author_name: "Kanye West",
                author_id: "9876",
                author_image: "images/kanye.jpg",
                content: "Wow, that's fly dude!",
                type: "raw",
                timestamp: "1423961198"
              },
              {
                id: UUID.v4(),
                author_name: "David Guetta",
                author_id: "2192",
                author_image: "images/david.jpg",
                content: "I dunno man, needs more Dub...",
                type: "markdown",
                timestamp: "1423962198"
              },
            ]}
        );

        return map;
    },

    newPost: function (post) {
        post["id"] = UUID.v4();
        this.posts.set(post["id"], post);
        // this.orderPosts();
        //TODO: ajax
        this.trigger(this.posts);
    },

    newComment: function (comment) {
        var post = this.posts.get(comment.post_id);
        post.comments.push(comment);
        //TODO: ajax
        this.trigger(this.posts);
    },

    orderPosts: function () {
        var ordered = this.posts.keys().sort(function(a, b) {
            a = this.posts[a];
            b = this.posts[b];
            if (a.timestamp < b.timestamp) {
                return -1;
            } else {
                return 1;
            }
        });
    }

});

module.exports = PostStore;
