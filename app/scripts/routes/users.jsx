import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { addons } from 'react/addons';
import { Col, Input } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';

import ListAuthors from '../components/list-authors';
import Spinner from '../components/spinner';

import { filterAuthors } from '../utils/helpers';

export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      authorsList : null,
      filterQuery : ''
    };
  },

  componentDidMount: function() {
    AuthorActions.getAuthors();
  },

  render: function() {
    if (_.isNull(this.state.authorsList)) {
      return (<Spinner />);
    }

    var filtered;

    if (_.isEmpty(_.trim(this.state.filterQuery))) {
      filtered = this.state.authorsList;
    } else {
      filtered = filterAuthors(this.state.authorsList, this.state.filterQuery);
    }

    return (
      <Col md={8} mdOffset={2}>
        <Input type="search" valueLink={this.linkState('filterQuery')} placeholder="Filter users..."/>
        <div className="well">
          <ListAuthors authors={filtered} />
        </div>
      </Col>
    );
  }
});
