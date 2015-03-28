import React from 'react';
import { Link } from 'react-router';
import { addons } from 'react/addons';

import AuthorStore from '../../stores/author';

export default React.createClass({
  mixins: [addons.PureRenderMixin],

  render: function() {
    var params;

    if (AuthorStore.isLoggedIn() &&
        AuthorStore.getAuthor().id === this.props.author.id) {
      params = {id: 'profile'};
    } else {
      params = { id: this.props.author.id,
                 host: encodeURIComponent(this.props.author.host) };
    }

    return (
      <Link to="author" params={params} title={this.props.author.host}>
        {this.props.children}
      </Link>
    );
  }
});
