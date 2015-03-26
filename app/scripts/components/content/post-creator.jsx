import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { Input } from 'react-bootstrap';
import Marked from 'marked';

import AuthorActions from '../../actions/author';
import ProfileLink from './profile-link';
// Responsible for creating posts and notifying the Author store when
// this happens.
export default React.createClass({

  mixins: [addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      contentType: "text/plain",
      visibility: "PUBLIC",
      preview: "",
      content: "",
      title: ""
    };
  },

  submitPost: function(evt) {
    evt.preventDefault();

    var post = _.clone(this.state);
    delete post.preview;

    // reset content state now that we have it stored
    this.setState(this.getInitialState());

    AuthorActions.createPost(post);
  },

  updatePreview: function(evt) {
    var content = this.state.content;

    switch(this.state.contentType) {
      case 'text/x-markdown':
        this.setState({preview: <div dangerouslySetInnerHTML={{__html: Marked(content)}} />});
        break;
      case 'text/html':
        this.setState({preview: <div dangerouslySetInnerHTML={{__html: content}} />});
        break;
      default:
        this.setState({preview: <p>{content}</p>});
    }
  },

  render: function() {

    // don't go further if we don't have our current author prop
    if (_.isNull(this.props.currentAuthor)) {
      return (<div></div>);
    }

    return (
      <div className="media">
        <div className="media-left">
          <ProfileLink author={this.props.currentAuthor}>
            <img className="media-object author-image" src={this.props.currentAuthor.getImage()}/>
          </ProfileLink>
        </div>
        <div className="media-body content-creator">
          <ul className="nav nav-tabs">
            <li role="presentation" className="active">
              <a href="#write-tab" aria-controls="write-tab" role="tab" data-toggle="tab">Write</a>
            </li>
            <li role="presentation" className="">
              <a href="#preview-tab" aria-controls="preview-tab" role="tab" data-toggle="tab" onClick={this.updatePreview}>Preview</a>
            </li>
          </ul>
          <div className="tab-content">
            <div role="tabpanel" className="tab-pane active" id="write-tab">
              <form onSubmit={this.submitPost} className="media-body content-creator">
                <Input type="text" placeholder="Title" valueLink={this.linkState('title')} required />
                <Input type="textarea" placeholder="Say something witty..." valueLink={this.linkState('content')}  required />
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
            <div role="tabpanel" className="tab-pane" id="preview-tab">
              <h4>{this.linkState('title')}</h4>
              {this.linkState('preview')}
            </div>
          </div>
        </div>
      </div>
    );
  }
});
