import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { Input, Col } from 'react-bootstrap';
import Marked from 'marked';

import AuthorActions from '../../actions/author';
import ProfileLink from './profile-link';

// Responsible for creating comments and notifying the Post store when
// this happens.
export default React.createClass({

  mixins: [addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      comment: ""
    };
  },

  submitComment: function(evt) {
    evt.preventDefault();

    // capture the current content in our inputs
    var content = _.clone(this.state);

    // reset content state now that we have it stored
    this.setState(this.getInitialState());

    // populate content with appropriate metadata
    AuthorActions.createComment(this.props.post, content);
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
        <form onSubmit={this.submitComment} className="media-body content-creator">
          <Col md={10}>
          <Input type="text" placeholder="Say something witty..." valueLink={this.linkState('comment')} required/>
          </Col>
          <Col md={2}>
            <Input className="pull-right" type="submit" value="Comment" />
          </Col>
        </form>
      </div>
    );
  }
});
