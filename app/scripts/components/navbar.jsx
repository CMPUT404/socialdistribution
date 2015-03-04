var React = require('react');
var Reflux = require('reflux');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var ReactRouterBootstrap = require('react-router-bootstrap')
  , NavItemLink = ReactRouterBootstrap.NavItemLink
var AuthorStore = require('../stores/author');

//TODO: Display the logged in author name with author_image in the navbar.
var Navigation = React.createClass({

  // mixins: [Reflux.connect(AuthorStore)],

  getInitialState: function() {
    return {
      // author: AuthorStore.getCurrentAuthor()
    };
  },

  render: function() {
    return (
      <Navbar brand="Social-Distribution">
        <Nav right>
          <NavItemLink to="/">Timeline</NavItemLink>
          <NavItemLink to="/profile">Profile</NavItemLink>
        </Nav>
      </Navbar>
    );
  }
});

module.exports = Navigation;
