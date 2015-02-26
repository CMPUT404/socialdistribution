var React = require('react');
var Reflux = require('reflux');
var Button= require('react-bootstrap').Button;

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

    console.log(posts);

    return (
      <div className="col-md-12 content-viewer">
        <Button onClick={this.refresh} type="submit">refresh</Button>
        <ul className="media-list">
          {posts}
        </ul>
      </div>
    );
  }
});

module.exports = ContentViewer;
