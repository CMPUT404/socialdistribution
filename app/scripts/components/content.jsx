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
    var content;
    var comments;

    if (this.props.data.comments) {
      comments = this.props.data.comments.map(function (comment) {
        return (
          <Content key={"comment-"+comment.id} data={comment} />
        );
      });
    }

    if (this.props.data.type == 'markdown') {
      content = <div dangerouslySetInnerHTML={{__html: Content.convertMarkdown(this.props.data.content)}} />;
    } else {
      content = <p>{this.props.data.content}</p>;
    }

    var timestamp = Moment.unix(this.props.data.timestamp).fromNow();

    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{id: this.props.data.author.id}}>
            <img className="media-object" src={this.props.data.author.image} style={Content.imgStyle} />
          </Link>
        </div>
        <div className="media-body">
          <h4 className="media-heading">{this.props.data.author.name}</h4>
          {content}
          <h6 className="timestamp">{timestamp}</h6>
          {comments}
        </div>
      </div>
    );
  }
});

export default Content;
