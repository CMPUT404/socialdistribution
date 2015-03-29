import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';

import { Input } from 'react-bootstrap';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';
import ProfileLink from './content/profile-link';

import { filterAuthors } from '../utils/helpers';

export default React.createClass({

  mixins: [Reflux.connect(AuthorStore)],

  getInitialState: function() {
    return {
      authorsList  : [],
      searchResults: []
    };
  },

  componentDidMount: function() {
    AuthorActions.getAuthors();

    document.addEventListener('click', this.clearOptions);
  },

  componentWillUnmount: function() {
    document.addEventListener('click', this.clearOptions);
  },

  clearOptions: function() {
    this.setState({searchResults: []});
  },


  onChange: function(evt) {
    this.setState({
      searchResults: filterAuthors(this.state.authorsList, evt.target.value)
                                  .slice(0, 12)
    });
  },

  onKeyDown: function(evt) {
    // escape key
    if (evt.keyCode == 27) {
      this.clearOptions();
    }
  },

  render: function() {
    var options;
    var results;

    results = this.state.searchResults.map((author) => {
      return (
        <li key={'result-' + author.id} className="text-nowrap">
          <ProfileLink author={author}>
            <span className="text-capitalize">{author.displayname}</span>
            <span className="text-lowercase light-text pull-right"> {author.host}</span>
          </ProfileLink>
        </li>
      );
    });

    if (results.length) {
      options = (
        <ul className="typeahead-options" onClick={this.clearOptions}>
          {results}
        </ul>
      );
    }

    return (
      <div className="typeahead">
        <Input type="search"
               onChange={this.onChange}
               onKeyDown={this.onKeyDown}
               placeholder="Search users..." />
        {options}
      </div>
    );
  }
});
