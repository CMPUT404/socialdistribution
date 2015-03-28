import _ from 'lodash';
import React from 'react';
import { NavItemLink } from 'react-router-bootstrap';
import { Navbar, Nav, NavItem, Input } from 'react-bootstrap';

import UserSearch from '../components/usersearch';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

import Notification from '../components/notification';

export default React.createClass({
  logout: function(evt) {
    AuthorActions.logout();
  },

  render: function() {
    var profileList;
    var navList;

    navList = [
      <NavItemLink key="posts" to="posts">
        <i className="fa fa-list"></i> Public Posts
       </NavItemLink>
    ];


    if (!_.isNull(this.props.currentAuthor)) {
      navList.unshift(
        <NavItemLink key="timeline" to="timeline">
        <i className="fa fa-list-alt"></i> Timeline
        </NavItemLink>
      );

      navList.push(
        <NavItem key="logout" onSelect={this.logout}>
        <i className="fa fa-sign-out"></i> Logout
        </NavItem>
      );
      //TODO: usersearch typeahead down here
      profileList = [
        <NavItem key="notifications" href="javascript:void(0)">
          <Notification />
        </NavItem>,
        <NavItemLink key="author" to="author" params={{id : 'profile'}}>
          <i className="fa fa-user"></i> <span className="text-capitalize">{this.props.currentAuthor.displayname}</span>
        </NavItemLink>
      ];
    } else {
      navList.push(
        <NavItemLink key="login"to="login">
        <i className="fa fa-sign-in"></i> Login
        </NavItemLink>
      )
    }

    navList.unshift(
      <form key="search" className="navbar-form navbar-left" role="search">
        <div className="form-group">
          <Input type="text" className="form-control" placeholder="Search authors..." />
        </div>
      </form>
    );


    return (
      <Navbar brand='Socshizzle'>
        <Nav navbar>
          {profileList}
        </Nav>
        <Nav navbar right>
          {navList}
        </Nav>
      </Navbar>
    );
  }
});
