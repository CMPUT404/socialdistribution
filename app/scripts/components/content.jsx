import React from 'react';
import Reflux from 'reflux';
import Moment from 'moment';
import { Link } from 'react-router';
import { markdown as Markdown } from 'markdown';
import { Col } from 'react-bootstrap';

// Represents an individual comment or post.
var Content = React.createClass({

  statics: {
    imgStyle: {
      width: '64px',
      height: '64px'
    },

    convertMarkdown: function(markdown) {
      return Markdown.toHTML(markdown);
    }
  },

  render: function() {
    var comments;

    if (this.props.data.comments) {
      comments = this.props.data.comments.map(function (comment) {
        return (
          <Content key={comment.id} data={comment} isPost={false} />
        );
      });
    }

    var timestamp = Moment.unix(this.props.data.timestamp).fromNow();

    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{authorId: this.props.data.author_id}}>
            <img className="media-object" src={this.props.data.author_image} style={Content.imgStyle} />
          </Link>
        </div>
        <div className="media-body">
          <h4 className="media-heading">{this.props.data.author_name}</h4>
          <p>{this.props.data.content}</p>
          <h6 className="timestamp">{timestamp}</h6>
          {comments}
        </div>
      </div>
    );
  }
});

export default Content;
