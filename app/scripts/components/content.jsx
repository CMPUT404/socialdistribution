import React from 'react';
import Reflux from 'reflux';
import Moment from 'moment';
import { Link } from 'react-router';
import { markdown as Markdown } from 'markdown';
import { Col } from 'react-bootstrap';

import ContentCreator from './contentcreator';

// Represents an individual comment or post.
var Content = React.createClass({

  convertMarkdown: function(markdown) {
    return Markdown.toHTML(markdown);
  },

  render: function() {
    var comments = [];

    if (this.props.data.comments) {
      comments = this.props.data.comments.map(function (comment) {
        return (
          <Content key={comment.id} data={comment} isPost={false} />
        );
      });
    }

    if (this.props.isPost) {
      comments.push(<ContentCreator key="comment-creator" post={this.props.data} forComment={true} />);
    }

    var timestamp = Moment.unix(this.props.data.timestamp).fromNow();

    return (
      <div className="media post">
        <div className="media-left">
          <Link to="author" params={{authorId: this.props.data.author_id}}>
            <img className="media-object author-image" src={this.props.data.author_image}/>
          </Link>
        </div>
        <div className="media-body">
          <h4 className="media-heading">{this.props.data.author_name}</h4>
          <p>{this.props.data.content}</p>
          <h6 className="timestamp">{timestamp}</h6>
        </div>
        <div className="comment-list">
          {comments}
        </div>
      </div>
    );
  }
});

export default Content;
