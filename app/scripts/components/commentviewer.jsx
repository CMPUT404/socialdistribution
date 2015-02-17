var React = require('react');
var Reflux = require('reflux');
var Content = require('./content');
var ContentCreator = require('./contentcreator');

var CommentViewer = React.createClass({

  render: function() {
    var comments = [];
    this.props.comments.forEach(function (comment) {
      comments.push(<Content key={comment.id} data={comment} />);
    });

    var forComment = true;
    comments.push();

    console.log("comments", comments);

    return (
      <ul className="media-list">
        {comments}
        <ContentCreator key={this.props.postId} forComment={forComment} />
      </ul>
    );
  }
});

module.exports = CommentViewer;
