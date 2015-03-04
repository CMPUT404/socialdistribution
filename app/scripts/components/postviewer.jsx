var React = require('react');
var Reflux = require('reflux');

var PostStore = require('../stores/post');
var PostActions = require('../actions/post');
var Content = require('./content');
var Button = require('react-bootstrap').Button;

var ContentViewer = React.createClass({

  mixins: [Reflux.connect(PostStore)],

  getInitialState: function() {
    return { posts: new Map() };
  },

  // when the component is loaded in the browser this is called automatically
  // and fetches posts asynchronously in the background
  componentDidMount: function() {
    this.refresh();
  },

  refresh: function() {
    var query = {author_id: this.props.authorId, author_only: false};
    if (this.props.isProfile) {
      query["author_only"] = true;
    }

    PostActions.refreshPosts(query);
  },

  render: function() {
    var posts = [];
    var isPost = true;

    this.state.posts.forEach(function (post, id) {
      posts.push(<Content key={id} data={post} isPost={isPost} />);
    });

    return (
      <div id="post-list">
        <Button type="button" onClick={this.refresh}>Refresh</Button>
        {posts}
      </div>
    );
  }
});

module.exports = PostViewer;
