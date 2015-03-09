import React from 'react';
import Reflux from 'reflux';
import { Navigation } from 'react-router';
import { NavItemLink } from 'react-router-bootstrap';
import { Navbar, Nav, NavItem} from 'react-bootstrap';

import UserSearch from './usersearch';
import AuthorActions from '../actions/author';

//TODO: Display the logged in author name with author_image in the navbar.
export default React.createClass({

  mixins: [Navigation],

  logOut: function(evt) {
    evt.preventDefault();
    AuthorActions.logOut();
    this.transitionTo('login');
  },

  render: function() {
    var currentAuthor  = this.props.author;
    var navList;

    if (currentAuthor) {
      navList = [
        <NavItemLink key="timeline" to="/">Timeline</NavItemLink>,
        <NavItemLink key="author" to="author" params={{id: currentAuthor.id}}>Profile</NavItemLink>,
        <NavItem key="logout" href="" onClick={this.logOut}>Logout</NavItem>
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
