var React = require('react');
var Reflux = require('reflux');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var ReactRouterBootstrap = require('react-router-bootstrap')
  , NavItemLink = ReactRouterBootstrap.NavItemLink
var AuthorStore = require('../stores/author');
var Router = require('react-router');

//TODO: Display the logged in author name with author_image in the navbar.
var Navigation = React.createClass({

  mixins: [Reflux.connect(AuthorStore),
           Router.Navigation],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  logOut: function(evt) {
    evt.preventDefault();
    AuthorStore.logOut();
    this.transitionTo('login');
  },

  render: function() {
    var currentAuthor  = this.state.currentAuthor;
    var navList;

    if (currentAuthor) {
      navList = [<NavItemLink key="timeline" to="/">Timeline</NavItemLink>,
                <NavItemLink key="author" to="author" params={{authorId: currentAuthor.id}}>Profile</NavItemLink>,
                <NavItem key="logout" href="" onClick={this.logOut}>Logout</NavItem>]
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

module.exports = Navigation;
