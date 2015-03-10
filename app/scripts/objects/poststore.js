import Check from 'check-types';

// This is sort of a custom datastore/container that makes it easier to deal
// with adding/removing/querying our post list.
export default class {

  constructor () {
    // a list of all posts in chronological order, simply reverse the array to
    // get the timeline
    this.allPosts = [];

    // map of authors to posts based on their index position in allPosts again
    // in chronological order, reverse the map value to get a user profile
    this.userMap = new Map();
  }

  // adds a post to the store and updates caches in various ways
  add (post) {

    if (Check.undefined(post.id) || Check.undefined(post.author.id)) {
      throw "Tried to add a post without a post or authorId";
    }

    // add post to the master list
    var length = this.allPosts.push(post);
    var allPostIndex = length - 1;

    // now update the user's post list
    var authorId = post.author.id;
    var userPosts = this.userMap.get(authorId);

    if (Check.undefined(userPosts)) {
      this.userMap.set(authorId, [allPostIndex]);
    } else {
      userPosts.push(allPostIndex);
    }
  }

  // removes a post from the store, a bit cumbersome
  removePost (post) {
    // first remove from user map
    var posts = this.userMap.get(post.author.id);
    var postIndex = posts.indexOf(post);
    var allPostsIndex = posts[postIndex];
    posts.slice(postIndex, 1);

    // now remove it from the master list
    this.allPosts.slice(allPostIndex, 1);
  }

  getTimeline (offset = 0, pagination = 25) {
    // return newest posts first
    return this.allPosts.reverse().slice(offset, offset + pagination);
  }

  // assumes that if this is being called, we have reason to believe that this
  // post exists for a given author
  getPost (authorId, postId) {

    // get author posts
    var postIndices = this.getPostsByAuthorId(authorId);

    // then find post in array
    for (let allPostIndex of postIndices) {
      var post = this.allPosts[allPostIndex];
      if (post.id == postId) {
        return post;
      }
    }

    // throw this because if we get here, the app logic is wrong
    throw "No post matching (authorId, postId): " + authorId + " - " + postId;
  }

  getPostsByAuthorId (authorId) {
    var posts = this.userMap.get(authorId);
    if (Check.undefined(posts)) {
      return [];
    }

    // if there is actually a set of posts here, return it in reverse order for
    // newest first
    return posts;
  }

  getAuthorViewPosts (authorId, offset = 0, pagination = 25) {
    return this.getPostsByAuthorId(authorId).reverse().slice(offset, offset + pagination);
  }
}
