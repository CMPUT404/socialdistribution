import chai from 'chai';

import PostStore from '../../app/scripts/objects/poststore';
import Post from '../../app/scripts/objects/post';

var should = chai.should();

describe('PostStore', function () {

  var postData = {
    id: "32n4j3h2bu3b",
    author: {
      id: "4567",
      name: "Benny Bennassi",
      image: "images/benny.jpg"
    },
    content: "Check out my new hit satisfaction",
    type: "raw",
    timestamp: "1423950298",
    comments: [{
      id: "9fn8sefh4hrnkw",
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
      id: "andinsif89s7gishn",
      author: {
        name: "David Guetta",
        id: "2192",
        image: "images/david.jpg"
      },
      content: "## I dunno man, needs more Dub...",
      type: "markdown",
      timestamp: "1424209498"
    }]
  };

  var postStore;
  var authorId = postData.author.id;
  var testPost = new Post(postData);

  beforeEach(function () {
    postStore = new PostStore();
  });

  describe('.add()', function () {
    it('should succesfully index a post for timeline and by user', function () {
      postStore.add(testPost);

      // basic length checks
      postStore.timeline.length.should.equal(1);
      postStore.authorMap.size.should.equal(1);

      var authorPosts = postStore.authorMap.get(postData.author.id);
      authorPosts.length.should.equal(1);
      authorPosts[0].should.deep.equal(testPost);

      // now make sure ordering works
      var post2 = new Post(postData);
      post2.id = "56tedg464etgert";

      postStore.add(post2);

      // two timeline posts, only one author in map
      postStore.timeline.length.should.equal(2);
      postStore.authorMap.size.should.equal(1);
      postStore.timeline[1].should.deep.equal(post2);
    });
  });

  describe('Post Getters', function () {

    var post2;

    beforeEach(function () {
      post2 = new Post(postData);
      post2.id = "sfmsjfndnfk434t";

      postStore.add(testPost);
      postStore.add(post2);
    });

    describe('.getPostsByAuthorId()', function () {
      it('should return all users posts', function () {
        var authorPosts = postStore.getPostsByAuthorId(authorId);
        authorPosts.length.should.equal(2);
      });
      it('should be in chronological order', function () {
        var authorPosts = postStore.getPostsByAuthorId(authorId);
        authorPosts[0].should.deep.equal(testPost);
      });
    });

    describe('.getPost()', function () {
      it('should return undefined if no post is found', function () {
        var post = postStore.getPost(postData.author.id, "badPostId");
        should.not.exist(post);
      });

      it('should successfully get an authors post', function () {
        var postId = postData.id;

        var post = postStore.getPost(authorId, postId);
        post.should.deep.equal(testPost);
      });
    });

    describe('.getTimeline()', function () {
      it('should return data in reverse chronological order', function () {
        var timeline = postStore.getTimeline();
        timeline.length.should.equal(2);
        timeline[1].should.deep.equal(testPost);
      });
    });

    describe('.getAuthorViewPosts()', function () {
      it('should return posts by newest first', function () {
        var posts = postStore.getAuthorViewPosts(authorId);
        posts[1].should.deep.equal(testPost);
      });
    });
  });

  describe('remove functionality', function () {
    var post2, post3;

    beforeEach(function () {
      post2 = new Post(postData);
      post2.id = "35sfg9gfdhng";
      post3 = new Post(postData);
      post3.id = "u9f9dnvdfkdf";

      postStore.add(post2);
      postStore.add(post3);
    });

    describe('.removePost()', function () {
      it('should remove the post from both stores', function () {
        postStore.remove(testPost);
        postStore.timeline.length.should.equal(2);

        // check ordering of stores
        var authorPosts = postStore.getPostsByAuthorId(authorId);
        authorPosts[0].should.deep.equal(post2);
        postStore.timeline[0].should.deep.equal(post2);
      });
    });
  });

});
