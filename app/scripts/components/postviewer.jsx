var React = require('react');
var Reflux = require('reflux');

var PostStore = require('../stores/post');
var PostActions = require('../actions/post');
var Content = require('./content');

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
        <button type="button" onClick={this.refresh} value="Refresh"/>
        {posts}
      </div>
    );
  }
});

module.exports = PostViewer;
