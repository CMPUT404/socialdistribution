import _ from 'lodash';
import React from 'react';
import Moment from 'moment';
import { Link } from 'react-router';
import { Col } from 'react-bootstrap';

import Spinner from '../spinner';

// Represents an individual comment
export default React.createClass({

  render: function() {
    if (_.isNull(this.props.data)) {
      return (<Spinner />);
    }

    return (
      <div className="media">
        <div className="media-left">
          <Link to="author" params={{id: this.props.data.author.id}}>
            <img className="media-object content-auth-img" src={this.props.data.author.getImage()} />
          </Link>
        </div>
        <div className="media-body">
          <Link to="author" params={{id: this.props.data.author.id}}>
            <h4 className="media-heading">{this.props.data.author.name}</h4>
          </Link>
          {this.props.data.comment}
          <h6 className="timestamp">{Moment(this.props.data.pubDate).fromNow()} by
            <Link to="author" params={{id: this.props.data.author.id}}>
              <span> {this.props.data.author.displayname}</span>
            </Link>
          </h6>
        </div>
      </div>
    );
  }
});
