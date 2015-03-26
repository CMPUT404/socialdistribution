import _ from 'lodash';
import React from 'react';
import Moment from 'moment';
import Marked from 'marked';
import { Col } from 'react-bootstrap';

import Spinner from '../spinner';

import Comment from './comment';
import ProfileLink from './profile-link';

// Represents an individual  post.
export default React.createClass({

  render: function() {
    var content, comments;

    if (_.isNull(this.props.data)) {
      return (<Spinner />);
    }

    if (this.props.data.hasComments()) {
      comments = this.props.data.getComments().map(function (comment) {
        return (
          <Comment key={"comment-"+comment.guid} data={comment} />
        );
      });
    }

    switch(this.props.data.contentType) {
      case 'text/x-markdown':
        content = <div dangerouslySetInnerHTML={{__html: Marked(this.props.data.content)}} />;
        break;
      case 'text/html':
        content = <div dangerouslySetInnerHTML={{__html: this.props.data.content}} />;
        break;
      default:
        content = <p>{this.props.data.content}</p>;
    }

    return (
      <div className="media">
        <div className="media-left">
          <ProfileLink author={this.props.data.author}>
            <img className="media-object content-auth-img" src={this.props.data.author.getImage()} />
          </ProfileLink>
        </div>
        <div className="media-body">
          <ProfileLink author={this.props.data.author}>
            <h4 className="media-heading">{this.props.data.author.name}</h4>
          </ProfileLink>
          <h4>{this.props.data.title}</h4>
          {content}
          <h6 className="timestamp">{Moment(this.props.data.pubDate).fromNow()} by
            <ProfileLink author={this.props.data.author}>
              <span> {this.props.data.author.displayname}</span>
            </ProfileLink>
          </h6>
          {comments}
        </div>
      </div>
    );
  }
});
