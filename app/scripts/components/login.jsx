import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { State, Navigation } from 'react-router';
import { Grid, Row, Col, Input, PageHeader } from 'react-bootstrap';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

export default React.createClass({

  mixins: [Reflux.listenTo(AuthorStore, "onUserChange"), State, Navigation],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  onUserChange: function(state) {
    if (Check.object(state.currentAuthor)) {
      this.transitionTo('timeline');
    }
  },

  statics: {
    // When an authenticated user tries to re-login
    willTransitionTo: function (transition, params) {
      if (Check.object(AuthorStore.getCurrentAuthor())) {
        //TODO: validate token
        transition.redirect('timeline');
      }
    }
  },

  usernameChange: function(evt) {
    this.setState({username: evt.target.value});
  },

  passwordChange: function(evt) {
    this.setState({password: evt.target.value});
  },

  logIn: function(evt) {
    evt.preventDefault();

    var username = this.state.username;
    var password = this.state.password;

    this.setState(this.getInitialState());

    AuthorActions.login(username, password);
  },

  render: function() {
    return (
      <Col md={6} mdOffset={3}>
        <Row><PageHeader>Login</PageHeader></Row>
        <Row>
          <form onSubmit={this.logIn}>
            <Input type="text"  label='Text' placeholder="Username" value={this.state.username} onChange={this.usernameChange} required/>
            <Input type="password" label='Password' placeholder="secret" value={this.state.password} onChange={this.passwordChange} required/>

            <Input className="center-block" type="submit" value="Login" />
          </form>
        </Row>
      </Col>
    );
  }
});
