import React from 'react';
import Reflux from 'reflux';
import { Navigation } from 'react-router';
import { Combobox as AutoComplete, ComboboxOption as Option } from 'react-autocomplete';

import AuthorStore from '../stores/author';

// Creates our UserSearch input
// Adapted from:
// https://github.com/rackt/react-autocomplete/blob/master/examples/basic/main.js
export default React.createClass({

  mixins: [Navigation, Reflux.connect(AuthorStore, "authorList")],

  getInitialState: function () {
    return {
      searchResults: [],
      authorList: [],
      search: "",
      selectedAuthor: null
    };
  },

  componentDidMount: function () {
    AuthorActions.getAuthorList();
  },

  filterByInput: function (search) {
    this.setState({selectedAuthorId: null}, function () {
      this.filterAuthors(search);
    }.bind(this));
  },

  // Handles Fuzzy Filtering Search Results
  filterAuthors: function (search) {

    // if empty search, no filtering
    if (search === '') {
      return this.setState({authors: this.state.authorList});
    } else {
      // Regex based on search that ignores case
      var filter = new RegExp('^' + search, 'i');

      // wait a little bit so that we don't waste ajax calls if the user keeps
      // typing
      setTimeout(function() {
        // not at all optimized, assumes we have the full list of authors
        // cached clientside
        this.setState({searchResults: this.state.authorList.filter(function (author) {
          return filter.test(author.name);
        })});
      }.bind(this), 300);
    }
  },

  // Handles transitioning the app to the author view if a user selects an
  // author from the search results
  onSelect: function (authorId) {
    this.transitionTo('author', {id: authorId});
  },

  renderSearchOptions: function () {
    return this.state.searchResults.map(function (author) {
      return (
        <Option key={author.id} value={author.id}>{author.name}</Option>
      );
    });
  },

  render: function () {

    // render search options
    var options;
    if (this.state.searchResults.length === 0) {
      options = <div className="empty-user-search" aria-live="polite">No matches.</div>;
    } else {
      options = this.renderSearchOptions();
    }

    return (
      <AutoComplete onInput={this.filterByInput} onSelect={this.onSelect} value={this.state.search}>
        {options}
      </AutoComplete>
    );
  }
});
