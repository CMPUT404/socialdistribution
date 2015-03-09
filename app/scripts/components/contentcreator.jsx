import React from 'react';
import Reflux from 'reflux';
import Moment from 'moment';
import { Link } from 'react-router';
import { Input } from 'react-bootstrap';
import { markdown as Markdown } from 'markdown';

import PostActions from '../actions/post';
import AuthorStore from '../stores/author';

// Responsible for creating posts/comments and notifying the Post store when
// this happens.
export default React.createClass({

  getInitialState: function() {
    return {
      content: this.defaultContent()
    };
  },

  defaultContent: function () {
    return {
      format: "markdown",
      content: ""
    };
  },

  formatChange: function(event) {
    this.setState({format: event.target.value});
  },

  contentChange: function(event) {
    this.setState({content: event.target.value});
  },

  submitContent: function() {

    // capture the current content in our inputs
    var content = {
      authorId: this.props.currentAuthor.id,
      content: this.state.content,
      format: this.state.format,
      timestamp: Moment.unix()
    };

    // reset content state now that we have it stored
    this.setState(this.getInitialState());

    // populate content with appropriate metadata
    if (this.props.forComment) {
      PostActions.newComment(this.props.post, content);
    } else {
      content.comments = [];
      PostActions.newPost(content);
    }
  },

  render: function() {
    var author = this.props.currentAuthor;
    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{authorId: author.id}}>
            <img className="media-object author-image" src={author.author_image}/>
          </Link>
        </div>
        <div className="media-body content-creator">
          <Input type="textarea" placeholder="Say something witty..." value={this.state.content.content} onChange={this.contentChange} />
          <Input type="select" label='Format' value={this.state.content.format} onChange={this.formatChange}>
            <option value="markdown">Markdown</option>
            <option value="text">Text</option>
            <option value="HTML">HTML</option>
          </Input>
          <Input className="pull-right" type="submit" value="Post" onClick={this.submitContent} />
        </div>
      </div>
    );
  }
});
