import _ from 'lodash';
import React from 'react';
import { Row, Col, Input, PageHeader } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';

// This the registration handler
export default React.createClass({

  statics: {
    // When an authenticated user tries to re-login
    willTransitionTo: function (transition, params) {
      // Using the author store is a hack, but until
      // https://github.com/rackt/react-router/pull/590 is merged/closed
      if (AuthorStore.isLoggedIn()) {
        transition.redirect("timeline");
      }
    }
  },

  getInitialState: function () {
    return {
      first_name      : "",
      last_name       : "",
      email           : "",
      displayname     : "",
      password        : "",
      bio             : "",
      github_username : ""
    };
  },

  firstNameChange   : function(evt) { this.setState({first_name: evt.target.value}); },
  lastNameChange    : function(evt) { this.setState({last_name: evt.target.value}); },
  emailChange       : function(evt) { this.setState({email: evt.target.value}); },
  displaynameChange : function(evt) { this.setState({displayname: evt.target.value}); },
  passwordChange    : function(evt) { this.setState({password: evt.target.value}); },
  bioChange         : function(evt) { this.setState({bio: evt.target.value}); },
  ghChange          : function(evt) { this.setState({github_username: evt.target.value}); },

  register: function(evt) {
    evt.preventDefault();

    var payload = _.clone(this.state);

    this.setState(this.getInitialState());

    AuthorActions.register(payload);
  },

  render: function() {
    return (
      <Col md={8} mdOffset={2}>
        <Row><PageHeader>Sign Up</PageHeader></Row>
        <Row>
          <form onSubmit={this.register}>
            <Input type="text" label='First Name' placeholder="first name" value={this.state.first_name} onChange={this.firstNameChange} required/>
            <Input type="text" label='Last Name' placeholder="last name" value={this.state.last_name} onChange={this.lastNameChange} required/>
            <Input type="email" label='Email' placeholder="email" value={this.state.email} onChange={this.emailChange} required/>
            <Input type="text"  label='Displayname' placeholder="Displayname" value={this.state.displayname} onChange={this.displaynameChange} required/>
            <Input type="password" label='Password' placeholder="secret" value={this.state.password} onChange={this.passwordChange} required/>
            <Input type="textarea" label='Bio' placeholder="Some stuff about yourself" value={this.state.bio} onChange={this.bioChange} required/>
            <Input type="text" label='GitHub Username' placeholder="username" value={this.state.github_username} onChange={this.ghChange} required/>

            <Input className="pull-right" bsStyle="primary" type="submit" value="Register" />
          </form>
        </Row>
      </Col>
    );
  }
});
