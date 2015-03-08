import React from 'react';
import Reflux from 'reflux';
import { Navigation } from 'react-router';

import Typeahead from './typeahead';
import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

// Creates our UserSearch input
// Adapted from:
// https://github.com/rackt/react-autocomplete/blob/master/examples/basic/main.js
export default React.createClass({

  mixins: [Navigation, Reflux.connect(AuthorStore)],

  getInitialState: function () {
    return {
      authorList: [],
      search: "",
      selectedAuthor: null
    };
  },

  componentDidMount: function () {
    AuthorActions.getAuthorNameList();
  },

  // Handles transitioning the app to the author view if a user selects an
  // author from the search results
  onSelect: function (authorName) {
    var authorId = AuthorStore.getAuthorIdByName(authorName);
    this.transitionTo('author', {id: authorId});
  },

  render: function () {
    return (
      <Typeahead
        options={this.state.authorList}
        onSelect={this.onSelect}
        placeholder="Find friends..." />
    );
  }
});
