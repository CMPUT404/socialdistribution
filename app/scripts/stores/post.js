import Reflux from 'reflux';
import UUID from 'uuid';
import Check from 'check-types';

import PostActions from '../actions/post';
import AuthorActions from '../actions/author';
import PostStore from '../objects/poststore';
import Post from '../objects/post';
import Comment from '../objects/comment';

// Deals with App State Machine state
export default Reflux.createStore({

  init: function() {
    // fetches the list of most recent posts
    this.postStore = new PostStore();

    // this helps us keep track of what author the user is currently viewing so
    // that we can push specific post updates when they are on that page
    this.authorViewId = undefined;

    // Listeners
    this.listenTo(PostActions.newPost, this.newPost);
    this.listenTo(PostActions.newComment, this.newComment);
    this.listenTo(PostActions.getTimeline, this.getTimeline);
    this.listenTo(PostActions.getAuthorPosts, this.getAuthorPosts);
    this.listenTo(AuthorActions.getAuthorAndListen, this.listenForAuthorPosts);
    this.listenTo(AuthorActions.unbindAuthorListener, this.unbindAuthorListener);
  },

  // Handles fetching posts based on query.
  getPosts: function () {
    // TODO: AJAX and remove defaultPost placeholder
    this.defaultPosts();
  },

  getTimeline: function (authorId) {
    //TODO: ajax
    this.pushPosts();
  },

  // used to find specific author posts for author views
  listenForAuthorPosts: function (authorId) {
    //TODO: retrive w/ ajax and cache

    // listen on author id
    this.authorViewId = authorId;
    this.pushPosts();
  },

  unbindAuthorListener: function () {
    this.authorViewId = undefined;
  },

  // Used to mock data out
  defaultPosts: function () {

    var uuid = UUID.v4();
    var post = new Post({
      id: uuid,
      author: {
        id: "4567",
        name: "Benny Bennassi",
        image: "images/benny.jpg"
      },
      content: "Check out my new hit satisfaction",
      type: "raw",
      timestamp: "1423950298",
      comments: [{
        id: UUID.v4(),
        author: {
          name: "Kanye West",
          id: "9876",
          image: "images/kanye.jpg"
        },
        content: "Wow, that's fly dude!",
        type: "raw",
        timestamp: "1424036698"
      },
      {
        id: UUID.v4(),
        author: {
          name: "David Guetta",
          id: "2192",
          image: "images/david.jpg"
        },
        content: "## I dunno man, needs more Dub...",
        type: "markdown",
        timestamp: "1424209498"
      }]
    });

    this.postStore.add(post);
  },

  newPost: function (post) {
    //TODO: ajax
    post["id"] = UUID.v4();
    this.postStore.add(post);
    this.pushPosts();
  },

  newComment: function (post, comment) {
    //TODO: ajax
    comment.id = UUID.v4();
    var post = this.postStore.getPost(post.author.id, post.id);
    post.comments.push(new Comment(comment));
    this.pushPosts();
  },

  // handles triggering updates since we want certain things to occur and might
  // have a listener active
  pushPosts: function (authorPosts) {
    var postTypes = {
      timeline: this.postStore.getTimeline()
    };

    // if we're currently listening for author posts
    if (!Check.undefined(this.authorViewId)) {
      console.log("here we are");
      postTypes.authorPosts = this.postStore.getPostsByAuthorId(this.authorViewId);
    }

    this.trigger(postTypes);
  }
});
