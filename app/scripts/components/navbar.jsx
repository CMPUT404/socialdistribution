import _ from 'lodash';
import React from 'react';
import { NavItemLink } from 'react-router-bootstrap';
import { Navbar, Nav, NavItem } from 'react-bootstrap';

import UserSearch from './usersearch';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

//TODO: Display the logged in author name with author_image in the navbar.
export default React.createClass({
  logout: function(evt) {
    AuthorActions.logout();
  },

  render: function() {
    var navList;

    if (!_.isNull(this.props.currentAuthor)) {
      navList = [
        <NavItemLink key="timeline" to="timeline">Timeline</NavItemLink>,
        <NavItemLink key="author" to="author" params={{id: this.props.currentAuthor.id}}>Profile</NavItemLink>,
        <NavItem key="logout" onSelect={this.logout}>Logout</NavItem>
      ];
    } else {
      navList = <NavItemLink to="login">Login</NavItemLink>;
    }

    return (
      <Navbar brand="Social-Distribution">
        <Nav right>
          {navList}
        </Nav>
      </Navbar>
    );
  }
});
