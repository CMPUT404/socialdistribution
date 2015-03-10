import _ from 'lodash';
import React from 'react';
import { Navigation } from 'react-router';
import { Grid, Row, Col, Input, PageHeader, Button } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';

export default React.createClass({

  mixins: [Navigation],

  statics: {
    // When an authenticated user tries to re-login
    willTransitionTo: function (transition, params) {
      // Using the author store is a hack, but until
      // https://github.com/rackt/react-router/pull/590 is merged/closed
      if (!_.isEmpty(AuthorStore.currentAuthor)) {
        transition.redirect("timeline");
      }
    }
  },

  getInitialState: function () {
    return {
      username: "",
      password: ""
    };
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

  toRegister: function(evt) {
    this.transitionTo('register');
  },

  render: function() {
    return (
      <Col md={6} mdOffset={3}>
        <Row>
          <PageHeader>Login</PageHeader>
          <Button className="pull-right" bsStyle="info" onClick={this.toRegister}>Sign Up?</Button>
        </Row>
        <Row>
          <form onSubmit={this.logIn}>
            <Input type="text"  label='Text' placeholder="Username" value={this.state.username} onChange={this.usernameChange} required/>
            <Input type="password" label='Password' placeholder="secret" value={this.state.password} onChange={this.passwordChange} required/>

            <Input className="pull-right" bsStyle="primary" type="submit" value="Login" />
          </form>
        </Row>
      </Col>
    );
  }
});
