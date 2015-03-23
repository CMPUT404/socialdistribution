import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import Moment from 'moment';
import { Link } from 'react-router';
import { markdown as Markdown } from 'markdown';
import { Col } from 'react-bootstrap';

import Spinner from '../spinner';

// Represents an individual comment or post.
var Content = React.createClass({

  statics: {
    convertMarkdown: function(markdown) {
      return Markdown.toHTML(markdown);
    }
  },

  render: function() {
    var content, comments, title;

    if (_.isNull(this.props.data)) {
      return (<Spinner />);
    }

    // by default, assume it's a comment
    content = <p>{this.props.data.comment}</p>;
    // overridden down here
    if (this.props.data.getType() === "Post") {
      title = this.props.data.title;
      if (this.props.data.hasComments()) {
        comments = this.props.data.getComments().map(function (comment) {
          return (
            <Content key={"comment-"+comment.guid} data={comment} />
          );
        });
      }

      switch(this.props.data.contentType) {
        case 'text/x-markdown':
          content = <div dangerouslySetInnerHTML={{__html: Content.convertMarkdown(this.props.data.content)}} />;
          break;
        case 'text/html':
          content = <div dangerouslySetInnerHTML={{__html: this.props.data.content}} />;
          break;
        default:
          content = <p>{this.props.data.content}</p>;
      }
    }

    // creates those nice "25 minutes ago" timestamps
    var timeSince = Moment(this.props.data.pubDate).fromNow();

    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{id: this.props.data.author.id}}>
            <img className="media-object content-auth-img" src={this.props.data.author.getImage()} />
          </Link>
        </div>
        <div className="media-body">
          <Link to="author" params={{id: this.props.data.author.id}}>
            <h4 className="media-heading">{this.props.data.author.name}</h4>
          </Link>
          <h4>{title}</h4>
          {content}
          <h6 className="timestamp">{timeSince} by
            <Link to="author" params={{id: this.props.data.author.id}}>
              <span> {this.props.data.author.displayname}</span>
            </Link>
          </h6>
          {comments}
        </div>
      </div>
    );
  }
});

export default Content;
