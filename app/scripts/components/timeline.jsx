import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { Col } from 'react-bootstrap';
import ContentViewer from './contentviewer';
import { State, Navigation } from 'react-router';

import AuthorStore from '../stores/author';
import ContentCreator from './contentcreator';

// Represents a collection of posts within the logged in user's social network.
export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), State, Navigation],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getCurrentAuthor()
    };
  },

  statics: {
    // Because this is a static method that's called before render
    // We have to use the global store get the state
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
      <Col md={12}>
        <div className="jumbotron">
          <h3>Mood?</h3>
          <ContentCreator authorId={this.state.currentAuthor.id} />
        </div>
        <ContentViewer authorId={this.state.currentAuthor.id} />
      </Col>
    );
  }
});
