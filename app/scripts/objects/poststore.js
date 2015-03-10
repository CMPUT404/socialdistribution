import Check from 'check-types';

// This is sort of a custom datastore/container that makes it easier to deal
// with adding/removing/querying our post list.
export default class {

  constructor () {
    // a list of all posts in chronological order, simply reverse the array to
    // get the timeline
    this.timeline = new Array();

    // map of authors to posts based on their index position in timeline again
    // in chronological order, reverse the map value to get a user profile
    this.authorMap = new Map();
  }

  // adds a post to the store and updates caches in various ways
  add (post) {

    if (Check.undefined(post.id) || Check.undefined(post.author.id)) {
      throw "Tried to add a post without a post or authorId";
    }

    // add post to the master list
    this.timeline.push(post);
    // now update the user's post list
    var authorId = post.author.id;
    var userPosts = this.authorMap.get(authorId);

    if (Check.undefined(userPosts)) {
      this.authorMap.set(authorId, [post]);
    } else {
      userPosts.push(post);
    }
  }

  // removes a post from the store, needs the full post object so we can figure
  // out author id
  remove (post) {
    // first remove from user map
    var posts = this.getPostsByAuthorId(post.author.id);
    var postIndex = posts.indexOf(post);

    // now remove from timeline
    var timelineIndex = this.timeline.indexOf(post);
    this.timeline.slice(timelineIndex, 1);
  }

  getTimeline (offset = 0, pagination = 25) {
    // make a copy of the array as not to reverse the real deal, then return newest
    // posts first
    var timeline = this.timeline.slice(0);
    return timeline.reverse();//.slice(offset, offset + pagination);
  }

  // assumes that if this is being called, we have reason to believe that this
  // post exists for a given author
  getPost (authorId, postId) {

    // get author posts
    var posts = this.getPostsByAuthorId(authorId);

    // then find post in array
    for (let post of posts) {
      if (post.id == postId) {
        return post;
      }
    }

    return undefined;
  }

  getPostsByAuthorId (authorId) {
    var posts = this.authorMap.get(authorId);
    if (Check.undefined(posts)) {
      return [];
    }

    // if there is actually a set of posts here, return it in reverse order for
    // newest first
    return posts;
  }

  getAuthorViewPosts (authorId, offset = 0, pagination = 25) {
    return this.getPostsByAuthorId(authorId).reverse();//.slice(offset, offset + pagination);
  }
}
