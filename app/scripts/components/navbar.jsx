var React = require('react');
var Reflux = require('reflux');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var NavItem = require('react-bootstrap').NavItem;
var AuthorStore = require('../stores/author');

var Timeline = React.createClass({

  mixins: [Reflux.connect(AuthorStore)],

  getInitialState: function() {
    return {
      author: AuthorStore.getAuthor()
    };
  },

  render: function() {
    return (
      <Navbar>
        <Nav>
          <NavItem eventKey={1} href="/timeline">Home</NavItem>
          <NavItem eventKey={2} href="/profile">Profile</NavItem>
        </Nav>
      </Navbar>
    );
  }
});

module.exports = Timeline;
