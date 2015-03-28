import React from 'react';
import Reflux from 'reflux';
import { addons } from 'react/addons';
import { Navigation } from 'react-router';
import { Row, Col, Input, PageHeader, Button } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';

import ActionListener from '../mixins/action-listener';

export default React.createClass({

  mixins: [Navigation, ActionListener, addons.LinkedStateMixin],

  statics: {
    // When an authenticated user tries to re-login
    willTransitionTo: function (transition, params) {
      if (AuthorStore.isLoggedIn()) {
        transition.redirect("timeline");
      }
    }
  },

  getInitialState: function () {
    return {
      username: '',
      password: ''
    };
  },

  componentDidMount: function() {
    this.listen(AuthorActions.login.complete, () => this.transitionTo('timeline'));
  },

  logIn: function(evt) {
    evt.preventDefault();

    var username = this.state.username;
    var password = this.state.password;

    this.setState(this.getInitialState());

    AuthorActions.login(username, password);
  },

  toRegister: function(evt) {
    this.transitionTo('register');
  },

  render: function() {
    return (
      <Col md={4} mdOffset={4} className="well">
        <Row>
          <h2 className="text-center">Login</h2>
        </Row>
        <Row>
          <form onSubmit={this.logIn}>
            <Input type="text" label="Username" placeholder="Username"  valueLink={this.linkState('username')} required/>
            <Input type="password" label='Password' placeholder="secret" valueLink={this.linkState('password')} required/>

            <Col md={6}><Button className="pull-left" bsStyle="default" onClick={this.toRegister}>Sign Up?</Button></Col>
            <Col md={6}><Input className="pull-right" bsStyle="primary" type="submit" value="Login" /></Col>
          </form>
        </Row>
      </Col>
    );
  }
});
