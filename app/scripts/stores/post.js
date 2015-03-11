import _ from 'lodash';
import Reflux from 'reflux';
import UUID from 'uuid';

import PostActions from '../actions/post';
import AuthorActions from '../actions/author';
import PostStore from '../objects/poststore';
import Post from '../objects/post';
import Comment from '../objects/comment';

// Deals with App State Machine state
export default Reflux.createStore({

  init: function() {
    // fetches the list of most recent posts
    // this.postStore = new PostStore();

    // this helps us keep track of what author the user is currently viewing so
    // that we can push specific post updates when they are on that page
    this.authorViewId = undefined;

    // TODO: remove this once we are populating our own data
    // this.getPosts();

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

  // fetches the timeline specific to the given author id
  getTimeline: function (authorId) {
    //TODO: ajax
    this.pushPosts();
  },

  // used to find specific author posts for author views
  listenForAuthorPosts: function (authorId) {
    //TODO: retrive w/ ajax and cache

    // listen on author id
    this.authorViewId = authorId;
    // this.pushPosts();
  },

  unbindAuthorListener: function () {
    this.authorViewId = undefined;
  },

  newPost: function (post) {
    //TODO: ajax
    post.id = UUID.v4();
    this.postStore.add(new Post(post));
    this.pushPosts();
  },

  newComment: function (post, comment) {
    //TODO: ajax
    comment.id = UUID.v4();
    var post = this.postStore.getPost(post.author.id, post.id);
    post.addComment(new Comment(comment));
    this.pushPosts();
  },

  // handles triggering updates since we want certain things to occur and might
  // have a listener active
  pushPosts: function (authorPosts) {
    var postTypes = {
      timeline: this.postStore.getTimeline()
    };

    // if we're currently listening for author posts
    if (!_.isUndefined(this.authorViewId)) {
      postTypes.authorPosts = this.postStore.getAuthorViewPosts(this.authorViewId);
    }

    this.trigger(postTypes);
  }
});
