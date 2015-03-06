import React from 'react';
import Reflux from 'reflux';
import Check from 'check-types';
import { State } from 'react-router';
import { Grid, Row, Col, Input, PageHeader } from 'react-bootstrap';

import AuthorStore from '../stores/author';



export default React.createClass({

  mixins: [Reflux.connect(AuthorStore), State],

  getInitialState: function() {
      return {
        currentAuthor: AuthorStore.getCurrentAuthor()
      };
  },

  statics: {
      // When an authenticated user tries to re-login
      willTransitionTo: function (transition, params) {
        if (Check.object(AuthorStore.getCurrentAuthor())) {
          //TODO: validate token
          transition.redirect('timeline');
        }
      }
  },

  render: function() {
    return (
      <Col md={6} mdOffset={3}>
        <Row><PageHeader>Login</PageHeader></Row>
        <Row>
          <form>
            <Input type="text" label='Text' defaultValue="Username" />
            <Input type="password" label='Password' defaultValue="secret" />
            <Input type="select" label='Server... Maybe' defaultValue="server">
              <option value="select">select</option>
              <option value="other">...</option>
            </Input>
            <Input className="center-block" type="submit" value="Submit button" />
          </form>
        </Row>
      </Col>
    );
  }
});
