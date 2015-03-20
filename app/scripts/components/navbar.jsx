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
    var navList = [<NavItemLink key="posts" to="posts">Posts</NavItemLink>]

    if (!_.isNull(this.props.currentAuthor)) {
      navList.unshift(
        <NavItemLink key="timeline" to="timeline">Timeline</NavItemLink>,
        <NavItemLink key="author" to="author" params={{id: this.props.currentAuthor.id}}>Profile</NavItemLink>
      );
      navList.push(
        <NavItem key="logout" onSelect={this.logout}>Logout</NavItem>);
    } else {
      navList.push(<NavItemLink key="login" to="login">Login</NavItemLink>);
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
