import _ from 'lodash';
import React from 'react';
import { Link } from 'react-router';
import { addons } from 'react/addons';
import { Input } from 'react-bootstrap';
import { markdown as Markdown } from 'markdown';

import AuthorActions from '../../actions/author';

// Responsible for creating posts and notifying the Author store when
// this happens.
export default React.createClass({

  mixins: [addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      contentType: "text/plain",
      visibility: "PUBLIC",
      content: "",
      title: ""
    };
  },

  submitPost: function(evt) {
    evt.preventDefault();

    var post = _.clone(this.state);

    // reset content state now that we have it stored
    this.setState(this.getInitialState());

    AuthorActions.createPost(post);
  },

  render: function() {

    // don't go further if we don't have our current author prop
    if (_.isNull(this.props.currentAuthor)) {
      return (<div></div>);
    }

    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{id: this.props.currentAuthor.id}}>
            <img className="media-object author-image" src={this.props.currentAuthor.getImage()}/>
          </Link>
        </div>
        <form onSubmit={this.submitPost} className="media-body content-creator">
          <Input type="text" placeholder="Title" valueLink={this.linkState('title')} required />
          <Input type="textarea" placeholder="Say something witty..." valueLink={this.linkState('content')} required />
          <Input label='Visibility' type="select" valueLink={this.linkState('visibility')}>
            <option value="PUBLIC">Public</option>
            <option value="FRIENDS">Friends Only</option>
            <option value="FOAF">Friends of Friends</option>
            <option value="FOH">Friends on My Host</option>
            <option value="SERVERONLY">Same Server</option>
          </Input>
          <Input label='Format' type="select" valueLink={this.linkState('contentType')}>
            <option value="text/x-markdown">Markdown</option>
            <option value="text/html">HTML</option>
            <option value="text/plain">Text</option>
          </Input>

          <Input className="pull-right" type="submit" value="Post" />
        </form>
      </div>
    );
  }
});
