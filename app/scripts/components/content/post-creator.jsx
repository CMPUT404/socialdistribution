import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { TabbedArea, TabPane, Input } from 'react-bootstrap';
import Marked from 'marked';

import AuthorActions from '../../actions/author';
import ImageReader from '../image-reader';
import ProfileLink from './profile-link';
// Responsible for creating posts and notifying the Author store when
// this happens.
export default React.createClass({

  mixins: [addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      contentType: 'text/plain',
      visibility : 'PUBLIC',
      preview    : '',
      content    : '',
      title      : '',
      image      : '',
      tabKey     : 1
    };
  },

  submitPost: function(evt) {
    evt.preventDefault();

    var post = _.clone(this.state);

    delete post.preview;
    delete post.tabKey;

    // reset content state now that we have it stored
    this.setState(this.getInitialState());
    this.refs.imageReader.reset();

    AuthorActions.createPost(post);
  },

  updatePreview: function(key) {
    this.setState({tabKey: key});

    if (key === 2) {
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
    }
  },

  setImage: function(image) {
    this.setState({image: image});
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
            <img className="media-object author-image" src={this.props.currentAuthor.image}/>
          </ProfileLink>
        </div>
        <div className="media-body content-creator">

          <TabbedArea activeKey={this.state.tabKey}  onSelect={this.updatePreview}>
            <TabPane eventKey={1} tab='Write'>
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
                <ImageReader ref="imageReader" onComplete={this.setImage} />
                <Input className="pull-right" type="submit" value="Post" />
              </form>
            </TabPane>
            <TabPane eventKey={2} tab='Preview'>
              <h4>{this.linkState('title')}</h4>
              {this.linkState('preview')}
            </TabPane>
          </TabbedArea>
        </div>
      </div>
    );
  }
});
