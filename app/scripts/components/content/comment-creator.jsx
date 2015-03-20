import _ from 'lodash';
import React from 'react';
import { Link } from 'react-router';
import { addons } from 'react/addons';
import { Input, Col } from 'react-bootstrap';
import { markdown as Markdown } from 'markdown';

import AuthorActions from '../../actions/author';

// NOT YET WORKING!!!!!

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

    content['post'] = this.props.post;

    // reset content state now that we have it stored
    this.setState(this.getInitialState());

    // populate content with appropriate metadata
    // AuthorActions.createComment(content);
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
