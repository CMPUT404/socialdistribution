import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { Navigation } from 'react-router';
import { NavItemLink, ButtonLink } from 'react-router-bootstrap';
import { Navbar, Nav, NavItem, ButtonToolbar, DropdownButton, MenuItem } from 'react-bootstrap';

import UserSearch from './usersearch';
import AuthorActions from '../actions/author';

//TODO: Display the logged in author name with author_image in the navbar.
export default React.createClass({

  mixins: [Navigation],

  // fires the logout action, transition is handled in layout
  logout: function(evt) {
    evt.preventDefault();
    AuthorActions.logout();
  },

  render: function() {
    var navList;

    if (!_.isEmpty(this.props.currentAuthor)) {
      navList = [
        <NavItemLink key="timeline" to="/">Timeline</NavItemLink>,
        <NavItemLink key="author" to="author" params={{id: this.props.currentAuthor.id}}>Profile</NavItemLink>,
        <NavItem key="logout" href="" onClick={this.logout}>Logout</NavItem>
      ];
    } else {
      navList = <NavItemLink key="logout" to="login">login</NavItemLink>;
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
