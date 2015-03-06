var React = require('react');
var Reflux = require('reflux');
var Check = require('check-types');
var Router = require('react-router');

var AuthorStore = require('../stores/author');
var ContentCreator = require('./contentcreator');
var ContentViewer = require('./contentviewer');

// Represents a collection of posts within the logged in user's social network.
var Timeline = React.createClass({

  mixins: [Reflux.connect(AuthorStore), Router.State, Router.Navigation],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  statics: {
    // Because this is a static method that's called before render
    // We have to use the gloabal store get the state
      willTransitionTo: function (transition, params) {
        if (Check.undefined(AuthorStore.getCurrentAuthor())) {
          transition.redirect('login');
        }
      }
  },

  // If a user logs out and causes a state change within
  // The current page then make sure render() doesn't update.
  // A transition will eventually occure...
  shouldComponentUpdate: function(nextProps, nextState) {
    if (Check.undefined(nextState.currentAuthor)) {
      return false;
    }
    return true
  },

  render: function() {
    return (
      <div className="col-md-12" id="timeline">
        <ContentCreator authorId={this.state.currentAuthor.id} />
        <ContentViewer authorId={this.state.currentAuthor.id} />
      </div>
    );
  }
});

module.exports = Timeline;
