import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { ListenerMixin } from 'reflux';
import { Modal, Button, Row, Col, Input } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';
import ImageReader from './image-reader';

export default React.createClass({
  mixins: [addons.PureRenderMixin, addons.LinkedStateMixin, ListenerMixin],

  getInitialState: function () {
    var author = AuthorStore.getAuthor();

    return {
      first_name      : author.first_name,
      last_name       : author.last_name,
      email           : author.email,
      bio             : author.bio,
      github_username : author.github_username,
      image           : ''
    };
  },

  componentDidMount: function() {
    this.listenTo(AuthorActions.update.complete, () => {
      alertify.success('Profile updated!');
      this.props.onRequestHide();
    });
  },

  submit: function() {
    if (_.isEmpty(this.state.image)) {
      delete this.state.image;
    }

    AuthorActions.update(_.clone(this.state));
  },

  setImage: function(image) {
    this.setState({image: image});
  },

  render: function() {
    return (
      <Modal {...this.props} title='Update Profile'>
        <div className="modal-body">
          <form onSubmit={this.sumbmit}>
            <Input type="text" label='First Name' placeholder="first name" valueLink={this.linkState('first_name')} />
            <Input type="text" label='Last Name' placeholder="last name" valueLink={this.linkState('last_name')} />
            <Input type="email" label='Email' placeholder="email" valueLink={this.linkState('email')} />
            <Input type="text" label='GitHub Username' placeholder="github username" valueLink={this.linkState('github_username')} />
            <Input type="textarea" label='Bio' placeholder="Some stuff about yourself" valueLink={this.linkState('bio')} />
            <ImageReader onComplete={this.setImage} />
          </form>
        </div>
        <div className="modal-footer">
          <Button onClick={this.props.onRequestHide}>Close</Button>
          <Button onClick={this.submit} bsStyle='primary'>Update</Button>
        </div>
      </Modal>
    );
  }
});
