import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { addons } from 'react/addons';
import { Button, Col, Row } from 'react-bootstrap';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

export default React.createClass({

  mixins: [Reflux.connect(AuthorStore)],

  getInitialState: function() {
    return {
      currentAuthor: AuthorStore.getAuthor(),
      friendStyle: 'success',
      followStyle: 'success'
    };
  },

  componentWillReceiveProps: function() {
    this.setState({
      friendStyle: 'success',
      followStyle: 'success'
    });
  },

  // this next bit is really ugly but there is no around it
  // unless if we split buttons into child components...

  setBtnStyle: function(btn, style) {
    switch(btn) {
      case 'friend': this.setState({friendStyle: style}); break;
      case 'follow': this.setState({followStyle: style}); break;
    }
  },

  onMouseOver: function(btn, style, value, evt) {
    this.setBtnStyle(btn, style);
    $(evt.target).html(value);
  },
  onMouseOut: function(btn, style, value, evt) {
    this.setBtnStyle(btn, style);
    $(evt.target).html(value);
  },

  unFollow: function() {
    AuthorActions.unfollowFriend(this.props.author);
  },

  follow: function() {
    AuthorActions.followFriend(this.props.author);
  },

  friend: function() {
    AuthorActions.addFriend(this.props.author);
  },

  render: function () {

    if (_.isNull(this.state.currentAuthor) ||
        this.state.currentAuthor.id === this.props.author.id) {
      return false;
    }

    var friend, follow;

    // see if the current author has already "friended" to the target author
    // under any context
    if (this.state.currentAuthor.inList('friends', this.props.author)) {
      return (
        <Row  className="pull-right row-padding">
          <Button onClick={this.unFollow}
                  bsStyle={this.state.friendStyle}
                  onMouseOut={this.onMouseOut.bind(this, 'friend', 'success', 'Friends')}
                  onMouseOver={this.onMouseOver.bind(this, 'friend', 'danger', 'Un-Friend')} >
            Friends
          </Button>
        </Row>
      );
    }

    if (this.state.currentAuthor.inList('following', this.props.author)) {
      follow = (
        <Button onClick={this.unFollow}
                bsStyle={this.state.followStyle}
                onMouseOut={this.onMouseOut.bind(this, 'follow', 'success', 'Following')}
                onMouseOver={this.onMouseOver.bind(this, 'follow', 'danger', 'Unfollow')} >
                Following
        </Button>
      );
    } else {
      follow = (
        <Button bsStyle="primary" onClick={this.follow}>
          Follow
        </Button>
      );
    }

    if (this.state.currentAuthor.inList('pending', this.props.author)) {
      friend = (
        <Button>Pending</Button>
      );
    } else {
      friend = (
        <Button bsStyle="primary" onClick={this.friend}>Add Friend</Button>
      );
    }

    return (
      <Row className="pull-right row-padding">
        <Col md={6}>{friend}</Col>
        <Col md={6}>{follow}</Col>
      </Row>
    );
  }
});
