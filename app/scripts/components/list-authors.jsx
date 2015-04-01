import _ from 'lodash';
import React from 'react';
import { Col, Row } from 'react-bootstrap';

import Subscribe from '../components/subscribe';
import ProfileLink from '../components/content/profile-link';

export default React.createClass({

  render: function() {
    if (_.isEmpty(this.props.authors)) {
      return false;
    }

    var authors = [];

    authors = this.props.authors.map((author) => {
      return (
        <li key={author.id} className="list-group-item">
          <div className="media">
            <div className="media-left">
              <ProfileLink author={author}>
                <img className="media-object author-image" src={author.image}/>
              </ProfileLink>
            </div>
            <Row className="media-body">
              <Col md={6}>
                <ProfileLink author={author}>
                  <h4 className="text-capitalize">{author.displayname}</h4>
                </ProfileLink>
                <h6 className="light-text">Host: {author.host}</h6>
              </Col>
              <Col md={6}>
                <Subscribe className="pull-right" author={author} />
              </Col>
            </Row>
          </div>
        </li>
      );
    });

    return (
      <ul className="list-group">
        {authors}
      </ul>
    );
  }
});
