import _ from 'lodash';
import React from 'react';
import { NavItemLink } from 'react-router-bootstrap';
import { Navbar, Nav, NavItem, Input } from 'react-bootstrap';

import UsersTypeahead from '../components/users-typeahead';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

import Notification from '../components/notification';

export default React.createClass({
  logout: function(evt) {
    AuthorActions.logout();
  },

  render: function() {
    var profileList = [];
    var navList;

    navList = [
      <NavItemLink  key="users" to="users">
        <i className="fa fa-users"></i> Users
      </NavItemLink>,
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

    profileList.push(
      <form key="search" className="navbar-form navbar-left" role="search">
        <div className="form-group">
          <UsersTypeahead />
        </div>
      </form>
    );


    return (
      <Navbar brand='Socshizzle' fixedTop>
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
