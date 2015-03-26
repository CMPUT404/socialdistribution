import _ from 'lodash';
import React from 'react';
import Reflux from 'reflux';
import { ButtonGroup, Button, Col } from 'react-bootstrap';

import AuthorStore from '../stores/author';
import AuthorActions from '../actions/author';

export default React.createClass({

  mixins: [Reflux.connect(AuthorStore)],

  getInitialState: function() {
    return {
      currentAuthor: null
    };
  },

  componentDidMount: function() {
    this.setState({
      currentAuthor: AuthorStore.getAuthor(),
      btnStyle: "success",
    });
  },

  onMouseOver: function(value, style, evt) {
    this.setState({btnStyle: style});
    $(evt.target).html(value);
  },
  onMouseOut: function(value, style, evt) {
    this.setState({btnStyle: style});
    $(evt.target).html(value);
  },

  unFollow: function() {
    AuthorActions.unfollowFriend(this.props.author.id);
  },

  follow: function() {
    AuthorActions.followFriend(this.props.author.id);
  },

  friend: function() {
    // Manual construction is needed for two reasons
    // 1. Privacy (currentAuthor has stuff we don't want to send)
    // 2. Crazy circular references that break JSON.stringify
    AuthorActions.addFriend({
      query: "friendrequest",
      author: {
        id         : this.state.currentAuthor.id,
        url        : this.state.currentAuthor.url,
        host       : this.state.currentAuthor.host,
        displayname: this.state.currentAuthor.displayname
      },
      friend: {
        id         : this.props.author.id,
        url        : this.props.author.url,
        host       : this.props.author.host,
        displayname: this.props.author.displayname
      }
    });
  },

  render: function () {

    if (_.isNull(this.state.currentAuthor)) {
      return false;
    }

    var friend, following;

    // see if the current author has already "friended" to the target author
    // under any context
    if (this.state.currentAuthor.hasFriend(this.props.author)) {
      return (
        <Button bsStyle={this.state.btnStyle}
                className="pull-right"
                onClick={this.unFollow}
                onMouseOut={this.onMouseOut.bind(this, 'Friends', 'success')}
                onMouseOver={this.onMouseOver.bind(this, 'Un-Friend', 'danger')} >
          Friends
        </Button>
      );
    }

    if (this.state.currentAuthor.follows(this.props.author)) {
      following = (
        <Button onClick={this.unFollow}
                bsStyle={this.state.btnStyle}
                onMouseOut={this.onMouseOut.bind(this, 'Following', 'success')}
                onMouseOver={this.onMouseOver.bind(this, 'Unfollow', 'danger')} >
                Following
        </Button>
      );
    } else {
      following = (
        <Button bsStyle="primary" onClick={this.follow}>
          Follow
        </Button>
      );
    }

    if (this.state.currentAuthor.pendingFriend(this.props.author)) {
      friend = (
        <Button>Pending</Button>
      );
    } else {
      friend = (
        <Button bsStyle="primary" onClick={this.friend}>Add Friend</Button>
      );
    }

    return (
      <div className="pull-right">
        <Col md={6}>{friend}</Col>
        <Col md={6}>{following}</Col>
      </div>
    );
  }
});
