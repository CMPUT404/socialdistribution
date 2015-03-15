import React from 'react';
import { Button } from 'react-bootstrap';

import AuthorActions from '../actions/author';

export default React.createClass({

  onClick: function (evt) {
    var action = evt.target.value;
    switch (action) {
      case 'Unfriend':
      case 'Unfollow':
        AuthorActions.unsubscribeFrom(this.props.author);
        break;
      case 'Follow':
      case 'Friend':
        AuthorActions.subscribeTo(this.props.author);
        break;
    }

    // hack to rerender follow button rather than making the whole app rerender
    // because the current user updates
    // TODO: remove this by usiung action-listener..
    setTimeout(function () {this.forceUpdate()}.bind(this), 50);
  },

  render: function () {

    var authorId = this.props.author;
    var text;
    var style = "success";

    // see if the current author has already "subscribed" to the target author
    // under any context
    if (this.props.currentAuthor.hasFriend(this.props.author)) {
      text = "Unfriend";
      style = "danger";
    } else if (this.props.currentAuthor.followedBy(this.props.author)) {
      text = "Friend";
    } else if (this.props.currentAuthor.follows(this.props.author)) {
      text = "Unfollow";
      style = "danger";
    } else {
      text = "Follow";
    }

    return (
      <Button bsStyle={style} value={text} onClick={this.onClick}>{text}</Button>
    );
  }
});
