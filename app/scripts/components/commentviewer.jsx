var React = require('react');
var Reflux = require('reflux');
var Content = require('./content');
var ContentCreator = require('./contentcreator');

// Slightly differen than the contentviewer, this could probably be merged with
// it.
var CommentViewer = React.createClass({

  render: function() {

    var comments = [];
    this.props.comments.forEach(function (comment) {
      comments.push(<Content key={comment.id} data={comment} />);
    });

    var forComment = true;

    return (
      <div className="comment-list">
        {comments}
        <ContentCreator key={this.props.postId} forComment={forComment} />
      </div>
    );
  }
});

module.exports = CommentViewer;
