import _ from 'lodash';
import React from 'react';
import { addons } from 'react/addons';
import { Navigation } from 'react-router';
import { Row, Col, Input, PageHeader } from 'react-bootstrap';

import AuthorActions from '../../actions/author';
import AuthorStore from '../../stores/author';

import ActionListener from '../../mixins/action-listener';

// This the registration handler
export default React.createClass({

  mixins: [Navigation, ActionListener, addons.LinkedStateMixin],

  statics: {
    // When an authenticated user tries to register?
    willTransitionTo: function (transition, params) {
      // Using the author store is a hack, but until
      // https://github.com/rackt/react-router/pull/590 is merged/closed
      if (AuthorStore.isLoggedIn()) {
        transition.redirect('timeline');
      }
    }
  },

  getInitialState: function () {
    return {
      first_name      : '',
      last_name       : '',
      email           : '',
      displayname     : '',
      password        : '',
      bio             : '',
      github_username : '',
      password_check  : ''
    };
  },

  componentDidMount: function() {
    // If registration is complete, transition away
    this.listen(AuthorActions.register.complete, () => this.transitionTo('posts'));
  },

  register: function(evt) {
    evt.preventDefault();

    if (this.state.password != this.state.password_check) {
      alertify.error("Passwords don't match");
      return;
    }

    // lets not send that
    delete this.state.password_check;

    // don't send empty field either
    _.forEach(this.state, (val, key) => {
      if (_.isEmpty(val)) {
        delete this.state[key];
      }
    });

    var payload = _.clone(this.state);

    this.setState(this.getInitialState());

    AuthorActions.register(payload);
  },

  render: function() {
    return (
      <Col md={4} mdOffset={4} className="well">
        <Row><h2 className="text-center">Sign Up</h2></Row>
        <Row>
          <form onSubmit={this.register}>
            <Input type="text"  label='Displayname *' placeholder="Displayname" valueLink={this.linkState('displayname')} required/>
            <Input type="password" label='Password *' placeholder="secret" valueLink={this.linkState('password')} required/>
            <Input type="password" label='Repeat Password *' placeholder="secret" valueLink={this.linkState('password_check')} required/>
            <Input type="text" label='First Name' placeholder="first name" valueLink={this.linkState('first_name')} />
            <Input type="text" label='Last Name' placeholder="last name" valueLink={this.linkState('last_name')} />
            <Input type="email" label='Email' placeholder="email" valueLink={this.linkState('email')} />
            <Input type="text" label='GitHub Username' placeholder="github username" valueLink={this.linkState('github_username')} />
            <Input type="textarea" label='Bio' placeholder="Some stuff about yourself" valueLink={this.linkState('bio')} />

            <p><strong>* Required Fields</strong></p>
            <Input className="pull-right" bsStyle="primary" type="submit" value="Register" />
          </form>
        </Row>
      </Col>
    );
  }
});
