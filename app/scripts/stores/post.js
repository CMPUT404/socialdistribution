import Reflux from 'reflux';
import UUID from 'uuid';
import PostActions from '../actions/post';

// Deals with App State Machine state
export default Reflux.createStore({

  init: function() {
    // fetches the list of most recent posts
    this.posts = this.getPosts();

    // Listeners
    this.listenTo(PostActions.newPost, this.newPost);
    this.listenTo(PostActions.newComment, this.newComment);
    this.listenTo(PostActions.getTimeline, this.getTimeline);
    this.listenTo(PostActions.getAuthorPosts, this.getAuthorPosts);
  },

  // Handles fetching posts based on query.
  getPosts: function (query) {
    // TODO: AJAX and remove defaultPost placeholder
    return this.defaultPosts();
  },

  getTimeline: function (authorId) {
    //TODO: ajax
    this.trigger({posts: this.orderPosts(this.posts)});
  },

  // used to find specific author posts for author views
  getAuthorPosts: function (authorId) {
    //TODO: ajax
    // this is just temporary for testing
    var authorPosts = [];
    for(var value of this.posts.values()) {
      if (value.author_id == authorId) {
        authorPosts.push(value);
      }
    }
    this.trigger({posts: authorPosts});
  },

  // Used to mock data out
  defaultPosts: function (query) {

    var map = new Map();
    var uuid = UUID.v4();

    map.set(UUID.v4(), {
        id: uuid,
        author_id: "452267",
        author_name: "Benny Bennassi",
        author_image: "images/benny.jpg",
        content: "Check out my new hit satisfaction",
        type: "raw",
        timestamp: "1422950298",
        comments: [{
          id: UUID.v4(),
          author_name: "Kanye West",
          author_id: "92876",
          author_image: "images/kanye.jpg",
          content: "Wow, that's fly dude!",
          type: "raw",
          timestamp: "1424032698"
        },
        {
          id: UUID.v4(),
          author_name: "David Guetta",
          author_id: "219222",
          author_image: "images/david.jpg",
          content: "I dunno man, needs more Dub...",
          type: "markdown",
          timestamp: "1424209198"
        }]
      }
    );

    map.set(uuid, {
        id: uuid,
        author_id: "4567",
        author_name: "Benny Bennassi",
        author_image: "images/benny.jpg",
        content: "Check out my new hit satisfaction",
        type: "raw",
        timestamp: "1423950298",
        comments: [{
          id: UUID.v4(),
          author_name: "Kanye West",
          author_id: "9876",
          author_image: "images/kanye.jpg",
          content: "Wow, that's fly dude!",
          type: "raw",
          timestamp: "1424036698"
        },
        {
          id: UUID.v4(),
          author_name: "David Guetta",
          author_id: "2192",
          author_image: "images/david.jpg",
          content: "I dunno man, needs more Dub...",
          type: "markdown",
          timestamp: "1424209498"
        }]
      }
    );

    return map;
  },

  newPost: function (post) {
    post["id"] = UUID.v4();
    this.posts.set(post["id"], post);
    // this.orderPosts();
    //TODO: ajax
    this.trigger({"posts": this.orderPosts(this.posts) });
  },

  newComment: function (post, comment) {
    // <Content> complains when this is missing, used as "key"
    comment.id = UUID.v4();
    post.comments.push(comment);
    //TODO: ajax
    this.trigger({"posts": this.orderPosts(this.posts) });
  },

  // sorts posts into reverse chronological order. Aka, newest first.
  orderPosts: function (posts) {

    var postArr = [];
    if (posts.size == 0) {
      return postArr;
    }

    for (var value of posts.values()) {
      postArr.push(value);
    }

    postArr.sort(function(a, b) {
      if (a.timestamp < b.timestamp) {
        return -1;
      } if (a.timestamp == b.timestamp) {
        return 0;
      } else {
        return 1;
      }
    });

    return postArr;
  }

});
