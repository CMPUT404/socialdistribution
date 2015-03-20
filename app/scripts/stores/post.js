import _ from 'lodash';
import Reflux from 'reflux';

import Request from '../utils/request';

import PostActions from '../actions/post';
// import AuthorActions from '../actions/author';
// import PostStore from '../objects/poststore';
import Post from '../objects/post';


// Deals with App State Machine state
export default Reflux.createStore({

  init: function() {
    // fetches the list of most recent posts
    // this.postStore = new PostStore();

    // this helps us keep track of what author the user is currently viewing so
    // that we can push specific post updates when they are on that page
    this.authorViewId = undefined;


    // Listeners
    this.listenTo(PostActions.getTimeline, 'onGetTimeline');
    this.listenTo(PostActions.getPublicPosts, 'onGetPubPosts');

    // this.listenTo(PostActions.getAuthorPosts, this.getAuthorPosts);
    // this.listenTo(AuthorActions.getAuthorAndListen, this.listenForAuthorPosts);
    // this.listenTo(AuthorActions.unbindAuthorListener, this.unbindAuthorListener);
  },

  // fetches timelines posts
  onGetTimeline: function () {
    // TODO: AJAX
  },

  // fetches public posts
  onGetPubPosts: function () {
    Request
      .get('http://localhost:8000/posts')
      .promise(this.pubPostsComplete, PostActions.getPublicPosts.fail)
  },

  pubPostsComplete: function(postsData) {
    var posts = this._responseToData(postsData);

    this.trigger({publicPosts: posts});
    PostActions.getPublicPosts.complete(posts);
  },


  _responseToData: function(postsData) {
    return postsData.posts.map((post) => {
      return new Post(post);
    });
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
  }
});
