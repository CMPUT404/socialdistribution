import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux'
import ProfileLink from './content/profile-link';
import { OverlayTrigger, Button, Popover } from 'react-bootstrap';

import AuthorActions from '../actions/author';
import AuthorStore from '../stores/author';

export default React.createClass({

  mixins: [Reflux.connect(AuthorStore)],

  getInitialState() {
    return {
      currentAuthor: null
    };
  },

  componentDidMount() {
    this.setState({
      currentAuthor: AuthorStore.getAuthor()
    });
  },

  hideOverlay() {
    this.refs.overlay.hide()
  },

  acceptRequest(friend) {
    AuthorActions.addFriend(friend);
  },

  render() {
    if (_.isNull(this.state.currentAuthor)) {
      return false;
    }

    var requests = [];
    var overlay;
    var title;

    title = 'No pending requests';

    if (!_.isEmpty(this.state.currentAuthor.requests)) {
      title = 'Pending Requests';
      requests = this.state.currentAuthor.requests.map((request) => {
        return (
          <li key={'notification-' + request.id} className="list-group-item">
            <span className="badge" onClick={this.acceptRequest.bind(this, request)}>
              Accept
            </span>
            <ProfileLink author={request}>
              <h4 className="text-capitalize">{request.displayname}</h4>
            </ProfileLink>
            <small className="light-text">from {request.host}</small>
          </li>
        );
      })
    }

    var overlay = (
      <Popover onClick={this.hideOverlay}
               title={<p className="text-center">{title}</p>}>
        <div className="list-group">
          {requests}
        </div>
      </Popover>
    );

    return (
      <OverlayTrigger ref="overlay"
                      trigger='click'
                      placement='bottom'
                      overlay={overlay}>
        <span>
          <i className="fa fa-users"></i> {requests.length ? requests.length : ''}
        </span>
      </OverlayTrigger>

    );
  }
});
